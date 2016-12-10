#!~/usr/bin/env python 
# -*- coding: utf-8 -*-

import datetime
import boto.ses.connection
import boto.ec2.cloudwatch
import re

# AWS APIを利用するためのパラメータ。
# 本番ではIAMロールを利用するすること
aws_access_key_id = ''
aws_secret_access_key = ''

# メールの変数
from_address = ''
to_address = ['']
reply_address = ['']

end    = datetime.datetime.utcnow()
start  = end - datetime.timedelta(days=1)
cost_dict = {}

# --------------------------------------------

def send_mail_by_ses(body):
    '''
    Amazon SESでメールを送信する
    '''
    
    conn = boto.ses.connection.SESConnection(aws_access_key_id,aws_secret_access_key)
    conn.send_email(from_address,
                   '先日のAWS利用料金',
                   body,
                   to_address,
                   format='html',
                   reply_addresses=reply_address)

# --------------------------------------------

def main():
  # cloudwatchと接続
  cloud_watch = boto.ec2.cloudwatch.CloudWatchConnection(
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                )

  # cloudwatchからAWS/Billingのメトリックを取得
  metrics = cloud_watch.list_metrics(
                namespace = 'AWS/Billing'
               )
  
  # メトリックの詳細を取得し、詳細ごとに値を取得する
  for metric in metrics:

    data = cloud_watch.get_metric_statistics(
             period = '3600',
             start_time = start,
             end_time = end,
             metric_name = 'EstimatedCharges',
             namespace = 'AWS/Billing',
             statistics = 'Maximum',
             dimensions = metric.dimensions
           )
    

    if metric.dimensions.has_key('ServiceName'):
      cost_dict[metric.dimensions['ServiceName'][0]] = data[0]['Maximum']
    else:
      cost_dict['Total:'] = data[0]['Maximum']

  # メール本文作成
  body = """\
<html>
  <head></head>
  <body>
    <p>[AWS]∀･)ｺﾝﾆﾁﾊ!!! </p>
    <p>先日までのAWS利用料（概算）をお伝えします。</p>
"""

  # 辞書から一つずつ要素を取り出して処理
  for service,value in cost_dict.iteritems():
    # たまーにTotalが0.0になるので、0．0の場合は表示しない
    if service is 'Total:' and value is not str('0.0'):
      body  += '<b><p>%s$%s</p></b>\n' % (service.encode('utf_8') ,value)

  body += '<p>詳細は以下の通りです。</p>\n'
  body += '<table>\n'

  # 各サービスの詳細をテーブルで表示
  for service,value in cost_dict.iteritems():
    if service is not 'Total:':
      body += '<tr>'
      body += '<td>%s</td>\n' % (service.encode('utf_8'))
      body += '<td>$%s</td>\n' % (value)
      body += '</tr>'

  body += '</table>\n'
  body += """\
  </body>
</html>
"""

  # SESでメールを送信する
  send_mail_by_ses(body)

if __name__ == "__main__":
  main()
