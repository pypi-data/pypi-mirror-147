import pika
import json
import pika.exceptions as pex
from influxdb_client import InfluxDBClient
import pandas as pd


class Consumer(object):

    def __init__(self, rmq_credentials, rmq_host, rmq_hb):
        """
        initiation method to connect to rabbit, execute run() to start worker

        :param rmq_credentials: rabbit credentials object for connecting
        :param rmq_host: host address
        :param rmq_hb: rabbit heartbeat interval
        """
        # rabbit connections
        self.rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rmq_host, port=5672, virtual_host='/', credentials=rmq_credentials, heartbeat=rmq_hb))
        self.channel = None
        self.sms_channel = None
        self.sms_exchange = None
        self.send_as_sms = False

    def run(self, rmq_exchange, rmq_queue='', rmq_ex_type='fanout', rmq_queue_exclusive=True, rmq_auto_ack=True,
            rmq_prefetch_count=0):
        """
        Function to run to start the consumer obtaining data from the rabbit queue / exchange

        :param rmq_exchange: name of exchange to connect to, must have
        :param rmq_queue: name of exchange to connect to, if a persistent queue then name it
        :param rmq_ex_type: the type of exchange it connects to, default is 'fanout'
        :param rmq_queue_exclusive: boolean to define is the queue is exclusive (true),
                                    i.e. only one consumer can connect. Default is True
        :param rmq_auto_ack: boolean to define if the queue should auto acknowledge message received.
                             Default it True for performance reasons (True cannot be used with
                             channel.basic_ack() in callback)
        :param rmq_prefetch_count: is the number of message the consumer will take from the queue at a time.
                                   Default is 0, i.e. take all the messages (unlimited)
        :return: n/a
        """

        # open up channel and exchange
        print('|| open up channel ||')
        self.channel = self.rmq_connection.channel()
        self.channel.exchange_declare(exchange=rmq_exchange, exchange_type=rmq_ex_type)

        # set the quality of service
        print('|| Setup up QoS on channel, prefetch count ' + str(rmq_prefetch_count) + ' ||')
        self.channel.basic_qos(prefetch_count=rmq_prefetch_count)

        # create queue which is connected to exchange
        result = self.channel.queue_declare(queue=rmq_queue, exclusive=rmq_queue_exclusive)
        queue_name = result.method.queue
        print('|| Queue declare ' + str(queue_name) + ' ||')
        self.channel.queue_bind(queue=queue_name, exchange=rmq_exchange)

        # start consuming messages
        print('|| Start Consuming ||')
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=rmq_auto_ack)
        self.channel.start_consuming()

    def start_sms_producer(self, exchange_name='SMS', exchange_type='fanout'):
        """
        function to connect to sms producer
        :param exchange_name: the name of the exchange to connect to, default is 'SMS'
        :param exchange_type: type of exchange connecting to, default is 'fanout'
        :return: None
        """
        # SMS message channel (producer)
        print('|| Declare SMS Producer ||')
        self.sms_exchange = exchange_name
        self.sms_channel = self.rmq_connection.channel()
        self.sms_channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        self.send_as_sms = True

    def send_sms(self, message, routing_key=''):
        """
        function to send a message to sms rabbit consumer
        :param message: the text message to be sent
        :param routing_key: the routing key for the exchange, default is '' (i.e. no routing key)
        :return: None
        """
        if self.send_as_sms:
            print('|| Send SMS || ' + str(message))
            self.sms_channel.basic_publish(exchange=self.sms_exchange,
                                           routing_key=routing_key,
                                           body=message)
        else:
            print('|| Send SMS NOT enabled ||')

    def send_orders(self, products, price, direction, funds, num_of_trades,
                    algo_tag, commission, order_type, exchange_flow, rmq_order_exchange='orders'):
        """
        1. calculate the size of each order
        2. send off order messages

        :param products: list of products which should be traded e.g. [BTC-GBP] or [BTC-GBP, ETH-BTC, ETH-GBP]
        :param price: list of prices to make each trade at, this is used of limit orders ONLY.
        :param direction: list of the base currency that is the traded e.g. [GBP] with a [BTC-GBP] products list
                          would buy BTC and a [BTC] would sell BTC to return GBP
        :param funds: the TOTAL amount of funds to be traded, can be broken down into smaller values (see trade_size)
        :param num_of_trades: the number of trades to make with the funds
        :param algo_tag: The name (str) of redis tag for the funds which are to be updated/
        :param commission: A list of the commision used on each order, it is used to calculate sizing etc. e.g [0.005]
        :param order_type: A list of order types to make, e.g. 'limit' or 'market'; ['limit', 'limit', 'market']
        :param exchange_flow: A list of exchanges to flow through e.g. ['cbpro', 'cbpro', 'binance']
        :param rmq_order_exchange: the name of the rabbit mq exchange for orders, default is 'orders'
        :return: n/a
        """

        # 1 calculate the size of each order
        trade_size = float(funds/num_of_trades)

        # send sms
        self.send_sms("Sending " + str(num_of_trades) + " to order exec for " + str(products) + ".\n" +
                      "Funds: " + str(funds) + ".\n" +
                      "Order Sizing: " + str(trade_size))

        # 2 loop through the number of orders to make and send to orders exchange
        for i in range(num_of_trades):
            msg = {'products': products,
                   'arbitration_flow': direction,
                   'price': price,
                   'commission': commission,
                   'order_type': order_type,
                   'exchange': exchange_flow,
                   'funds': trade_size,
                   'algo_tag': algo_tag}
            # DEBUG print("order number " + str(i))
            print(msg)

            try:
                self.channel.basic_publish(exchange=rmq_order_exchange, routing_key='', body=json.dumps(msg))
            except pex.ChannelClosedByBroker:
                print("Order exchange does not exist and must be created by order consumer for QoS reasons")
                raise

    def callback(self, ch, method, properties, body: json):
        """
        needs to be defined for each used of the parent class
        """
        None


class InfluxDB:

    def __init__(self, token, org, url='http://localhost:8086'):
        self._client = InfluxDBClient(url=url, token=token, org=org)
        self._org = org
        self._query_api = self._client.query_api()

    def build_measurments_query(self, measurements):
        # setup query base
        query = "|> filter(fn: (r) =>"
        # loop through each item in the list, if the first one then no need for or, all other need or
        for i, m in enumerate(measurements):
            if i == 0:
                query = query + ' r._measurement == "' + str(m) + '"'
            else:
                query = query + ' or r._measurement == "' + str(m) + '"'
        query = query + ')'  # add final braket on
        # print(query)
        return query

    def build_fields_query(self, fields):
        # setup query base
        query = "|> filter(fn: (r) =>"
        # loop through each item in the list, if the first one then no need for or, all other need or
        for i, f in enumerate(fields):
            if i == 0:
                query = query + ' r._field == "' + str(f) + '"'
            else:
                query = query + ' or r._field == "' + str(f) + '"'
        query = query + ')'  # add final braket on
        # print(query)
        return query

    def build_range_query(self, start, end=''):
        # setup query base
        query = '|> range(start: ' + str(start)
        if end: query = query + ', stop: ' + str(end)
        query = query + ')'
        # print(query)
        return query

    def build_custom_fields_query(self, custom_field_text):
        if custom_field_text != "":
            query = '|> filter(fn: (r) => ' + str(custom_field_text)
            query = query + ')'
        else:
            query = ''

        return query

    def build_aggregate_query(self, window='', fn='mean', offset=''):
        if window and offset:
            query = '|> aggregateWindow(every: ' + str(window) + \
                    ', offset: ' + str(offset) + \
                    ', fn: ' + str(fn) + ', createEmpty: false)'
        elif window and not offset:
            query = '|> aggregateWindow(every: ' + str(window) + \
                    ', fn: ' + str(fn) + ', createEmpty: false)'
        else:
            query = ''
        # print(query)
        return query

    def build_yeilds_query(self, name=''):
        if name:
            return '|> yield(name: "' + str(name) + '")'
        else:
            return ''

    def get_average(self, bucket, start, measurements, fields,
                    end='', window=''):

        return self.get_trades(bucket, start, measurements, fields,
                               end, window)['_value'].mean()

    def get_trades(self, bucket, start, measurements, fields,
                   end='', window='', offset='', return_std_df=False, fn='mean', name='',
                   custom_field=''):
        # build up query with sub fuctions
        range_q = self.build_range_query(start, end)
        meseaurements_q = self.build_measurments_query(measurements)
        fields_q = self.build_fields_query(fields)
        custom_field_q = self.build_custom_fields_query(custom_field)
        aggregates_q = self.build_aggregate_query(window=window, fn=fn, offset=offset)
        yeilds_q = self.build_yeilds_query(name)

        # combine all sub queries to create complete one
        query = 'from(bucket: "' + str(bucket) + '")' \
                + str(range_q) \
                + str(meseaurements_q) \
                + str(fields_q) \
                + str(custom_field_q) \
                + str(aggregates_q) \
                + str(yeilds_q)

        # print(query)
        if return_std_df:
            return self.flux_df_into_std_df(self._query_api.query_data_frame(org=self._org, query=query))
        else:
            return self._query_api.query_data_frame(org=self._org, query=query)

    def get_volumes(self, bucket, start, measurements, fields,
                    end='', window='', offset='', return_std_df=True, name=''):

        # get the min and max value for each time peroid
        open = self.get_trades(bucket, start, measurements, fields, end, window, offset, return_std_df,
                               fn='min', name=name)
        close = self.get_trades(bucket, start, measurements, fields, end, window, offset, return_std_df,
                                fn='max', name=name)

        # loop through each ticker and create dictionay with deltas
        volumes = {}
        for m in measurements:
            volumes[m] = close[m] - open[m]

        return volumes

    def get_hloc(self, bucket, start, measurements, fields,
                 end='', window='', offset='', custom_field='') -> pd.DataFrame:
        """
        returns a dictionary of coin, with key of the coin and value of panda dataframe
        """

        high = self.get_trades(bucket, start, measurements, ['price'], end, window,
                               return_std_df=True, fn="max", name="high", offset=offset, custom_field=custom_field)
        low = self.get_trades(bucket, start, measurements, ['price'], end, window,
                              return_std_df=True, fn="min", name="low", offset=offset, custom_field=custom_field)
        open = self.get_trades(bucket, start, measurements, ['price'], end, window,
                               return_std_df=True, fn="first", name="open", offset=offset, custom_field=custom_field)
        close = self.get_trades(bucket, start, measurements, ['price'], end, window,
                                return_std_df=True, fn="last", name="close", offset=offset, custom_field=custom_field)

        for i in high.values(): i.rename(columns={'price': 'High'}, inplace=True)
        for i in low.values(): i.rename(columns={'price': 'Low'}, inplace=True)
        for i in open.values(): i.rename(columns={'price': 'Open'}, inplace=True)
        for i in close.values(): i.rename(columns={'price': 'Close'}, inplace=True)

        # remove price from measurements and generate columns for those fields
        fields.remove('price')
        extra_df = False
        if len(fields) > 0:
            others = self.get_trades(bucket, start, measurements, fields, end, window, custom_field=custom_field,
                                     return_std_df=True, fn="last")
            extra_df = True

        # create a standard dataframe for each coin
        hloc_dict = {}
        for m in measurements:
            df = pd.merge(high[m], low[m], on="Datetime")
            df = pd.merge(df, open[m], on="Datetime")
            df = pd.merge(df, close[m], on="Datetime")
            # if there are extra data frames then add these in
            if extra_df:
                df = pd.merge(df, others[m], on="Datetime")
            hloc_dict[m] = df

            # print(df.isna().sum().sum())

        return hloc_dict

    def flux_df_into_std_df(self, df):

        # extract coins to create the data frames and create dictionary for dataframes coming back
        coins = df._measurement.unique()
        dict_of_df = {}

        for c in coins:
            # extract coins from the query
            sub_df = df.loc[df['_measurement'] == c]
            # extract fields, i.e. price or volumes
            columns = sub_df._field.unique()
            # extract the times for the index
            index = sub_df._time.unique()

            # setup the dataframe
            std_df = pd.DataFrame(columns=columns, index=index)

            # loop through each field of column to build the dataframe
            for col in columns:
                # extract on the data for that field and set index to time to allow mapping
                sub_sub_df = sub_df.loc[sub_df['_field'] == col]
                sub_sub_df.set_index('_time', inplace=True, drop=True)
                std_df.index.names = ['Datetime']
                # new the index is set then drop in the values
                std_df[col] = sub_sub_df['_value']

            # put into dictionary
            dict_of_df[c] = std_df

        return dict_of_df
