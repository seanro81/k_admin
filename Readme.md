Отчет Балансировка партиций и диагностика кластера
================================================================================================================
  - Балансировка партиций и диагностика кластера
    - Артефакт проекта для настройки распределения партиций reassignment/reassignment.json    
    
    --Создайте новый топик balanced_topic с 8 партициями и фактором репликации 3.
         kafka-topics.sh --bootstrap-server localhost:9094 --topic balanced_topic --create --partitions 8 --replication-factor 3
    --Определите текущее распределение партиций.
         kafka-topics.sh --bootstrap-server localhost:9094 --describe --topic balanced_topic

		  kafka-topics.sh --bootstrap-server localhost:9094 --describe --topic balanced_topic
[2025-03-23 17:23:52,281] WARN [AdminClient clientId=adminclient-1] Connection to node 2 (/127.0.0.1:9096) could not be established. Node may not be available. (org.apache.kafka.clients.NetworkClient)
[2025-03-23 17:23:52,283] WARN [AdminClient clientId=adminclient-1] Connection to node 1 (/127.0.0.1:9095) could not be established. Node may not be available. (org.apache.kafka.clients.NetworkClient)
Topic: balanced_topic   TopicId: XQFMvreLSbS_veXFbIwFlQ PartitionCount: 8       ReplicationFactor: 3    Configs:
        Topic: balanced_topic   Partition: 0    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0
        Topic: balanced_topic   Partition: 1    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1
        Topic: balanced_topic   Partition: 2    Leader: 0       Replicas: 0,1,2 Isr: 0,1,2
        Topic: balanced_topic   Partition: 3    Leader: 2       Replicas: 2,1,0 Isr: 2,1,0
        Topic: balanced_topic   Partition: 4    Leader: 1       Replicas: 1,0,2 Isr: 1,0,2
        Topic: balanced_topic   Partition: 5    Leader: 0       Replicas: 0,2,1 Isr: 0,2,1
        Topic: balanced_topic   Partition: 6    Leader: 2       Replicas: 2,1,0 Isr: 2,1,0
        Topic: balanced_topic   Partition: 7    Leader: 1       Replicas: 1,0,2 Isr: 1,0,2
   
   --Перераспределите партиции.

    kafka-reassign-partitions.sh \
--bootstrap-server localhost:9094 \
--broker-list "1,2,3" \
--topics-to-move-json-file "/opt/reassignment/reassignment.json" \
--generate

Current partition replica assignment
{"version":1,"partitions":[]}

запуск
kafka-reassign-partitions.sh --bootstrap-server localhost:9094 --reassignment-json-file /tmp/reassignment.json --execute

$ kafka-reassign-partitions.sh --bootstrap-server localhost:9094 --reassignment-json-file /tmp/reassignment.json --execute
[2025-03-23 18:06:07,367] WARN [AdminClient clientId=reassign-partitions-tool] Connection to node 1 (/127.0.0.1:9095) could not be established. Node may not be available. (org.apache.kafka.clients.NetworkClient)
[2025-03-23 18:06:07,370] WARN [AdminClient clientId=reassign-partitions-tool] Connection to node 2 (/127.0.0.1:9096) could not be established. Node may not be available. (org.apache.kafka.clients.NetworkClient)
[2025-03-23 18:06:07,425] WARN [AdminClient clientId=reassign-partitions-tool] Connection to node 1 (/127.0.0.1:9095) could not be established. Node may not be available. (org.apache.kafka.clients.NetworkClient)
Current partition replica assignment

{"version":1,"partitions":[{"topic":"balanced_topic","partition":0,"replicas":[1,2,0],"log_dirs":["any","any","any"]},{"topic":"balanced_topic","partition":1,"replicas":[2,0,1],"log_dirs":["any","any","any"]},{"topic":"balanced_topic","partition":2,"replicas":[0,1,2],"log_dirs":["any","any","any"]},{"topic":"balanced_topic","partition":3,"replicas":[2,1,0],"log_dirs":["any","any","any"]},{"topic":"balanced_topic","partition":4,"replicas":[1,0,2],"log_dirs":["any","any","any"]},{"topic":"balanced_topic","partition":5,"replicas":[0,2,1],"log_dirs":["any","any","any"]},{"topic":"balanced_topic","partition":6,"replicas":[2,1,0],"log_dirs":["any","any","any"]},{"topic":"balanced_topic","partition":7,"replicas":[1,0,2],"log_dirs":["any","any","any"]}]}


      Проверьте статус перераспределения.
      Убедитесь, что конфигурация изменилась.

[2025-03-23 18:07:13,404] WARN [AdminClient clientId=adminclient-1] Connection to node 2 (/127.0.0.1:9096) could not be established. Node may not be available. (org.apache.kafka.clients.NetworkClient)
[2025-03-23 18:07:13,407] WARN [AdminClient clientId=adminclient-1] Connection to node 1 (/127.0.0.1:9095) could not be established. Node may not be available. (org.apache.kafka.clients.NetworkClient)
Topic: balanced_topic   TopicId: XQFMvreLSbS_veXFbIwFlQ PartitionCount: 8       ReplicationFactor: 3    Configs:
        Topic: balanced_topic   Partition: 0    Leader: 1       Replicas: 0,1,2 Isr: 1,2,0
        Topic: balanced_topic   Partition: 1    Leader: 2       Replicas: 1,2,0 Isr: 2,0,1
        Topic: balanced_topic   Partition: 2    Leader: 0       Replicas: 2,0,1 Isr: 0,1,2
        Topic: balanced_topic   Partition: 3    Leader: 2       Replicas: 1,0,2 Isr: 2,1,0
        Topic: balanced_topic   Partition: 4    Leader: 1       Replicas: 0,2,1 Isr: 1,0,2
        Topic: balanced_topic   Partition: 5    Leader: 0       Replicas: 1,2,0 Isr: 0,2,1
        Topic: balanced_topic   Partition: 6    Leader: 2       Replicas: 2,0,1 Isr: 2,1,0
        Topic: balanced_topic   Partition: 7    Leader: 1       Replicas: 2,1,0 Isr: 1,0,2



   --Смоделируйте сбой брокера:
     a.  Остановите брокер kafka-1.
	 docker stop kafka-1

     b.  Проверьте состояние топиков после сбоя. на kafka-0
	 kafka-topics.sh --bootstrap-server localhost:9092 --list
	 $ kafka-topics.sh --bootstrap-server localhost:9094 --describe --topic balanced_topic

	 kafka-topics.sh --bootstrap-server localhost:9094 --describe --topic balanced_topic
[2025-03-24 17:07:56,956] WARN [AdminClient clientId=adminclient-1] Connection to node 2 (/127.0.0.1:9096) could not be established. Node may not be available. (org.apache.kafka.clients.NetworkClient)
[2025-03-24 17:07:57,003] WARN [AdminClient clientId=adminclient-1] Connection to node 2 (/127.0.0.1:9096) could not be established. Node may not be available. (org.apache.kafka.clients.NetworkClient)
Topic: balanced_topic   TopicId: OACaktHYTGq2P4did61C9w PartitionCount: 8       ReplicationFactor: 3    Configs:
        Topic: balanced_topic   Partition: 0    Leader: 0       Replicas: 0,1,2 Isr: 2,0
        Topic: balanced_topic   Partition: 1    Leader: 2       Replicas: 1,2,0 Isr: 2,0
        Topic: balanced_topic   Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 0,2
        Topic: balanced_topic   Partition: 3    Leader: 0       Replicas: 1,0,2 Isr: 0,2
        Topic: balanced_topic   Partition: 4    Leader: 0       Replicas: 0,2,1 Isr: 2,0
        Topic: balanced_topic   Partition: 5    Leader: 2       Replicas: 1,2,0 Isr: 0,2
        Topic: balanced_topic   Partition: 6    Leader: 2       Replicas: 2,0,1 Isr: 2,0
        Topic: balanced_topic   Partition: 7    Leader: 2       Replicas: 2,1,0 Isr: 2,0

     c.  Запустите брокер заново.
	 docker start kafka-1

     d.  Проверьте, восстановилась ли синхронизация реплик.

	 Topic: balanced_topic   TopicId: OACaktHYTGq2P4did61C9w PartitionCount: 8       ReplicationFactor: 3    Configs:
        Topic: balanced_topic   Partition: 0    Leader: 0       Replicas: 0,1,2 Isr: 2,0,1
        Topic: balanced_topic   Partition: 1    Leader: 2       Replicas: 1,2,0 Isr: 2,0,1
        Topic: balanced_topic   Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 0,2,1
        Topic: balanced_topic   Partition: 3    Leader: 0       Replicas: 1,0,2 Isr: 0,2,1
        Topic: balanced_topic   Partition: 4    Leader: 0       Replicas: 0,2,1 Isr: 2,0,1
        Topic: balanced_topic   Partition: 5    Leader: 2       Replicas: 1,2,0 Isr: 0,2,1
        Topic: balanced_topic   Partition: 6    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1
        Topic: balanced_topic   Partition: 7    Leader: 2       Replicas: 2,1,0 Isr: 2,0,1
 

Отчет настройка SSL/SASL/ACL на ZooKeeper  
==================================================================================================================
         Артефакты проекта
        - /ca               Сомоподписанный сертификат и ключ
        - /kafka-0-kreds    Серверный сертификат подписанный /ca
        - /kafka-1-kreds    Серверный сертификат подписанный /ca
        - /kafka-2-kreds    Серверный сертификат подписанный /ca
        - /jaas_conf/kafka_server_jaas.conf   учетные записи для доступа к zookeeper из kafka
                                              учетные записи для доступа к kafka
        - /jaas_conf_zoo/zookeeper_server_jaas.conf  учетные записи для доступа к zookeeper
        - /app  - python сервис с настроенным ssl sals соединением на основе сертификата из /ca

         Лог клиенского приложения с успешой авторизацией SASL пользователя admin по SSL 
          
         (venv) C:\Users\Andre\Desktop\Архитектура\KAFKA_COURSE\DZ_4_kafka_admin\k_admin\app>python main.py
             20:21:27: Инициализация коннекта - отправка сообщений
             20:21:27: Sending username and password in the clear
             20:21:27: Authenticated as admin via PLAIN
             20:21:27: Sending username and password in the clear
             20:21:27: Authenticated as admin via PLAIN
             20:21:27: Sending username and password in the clear
             20:21:27: Authenticated as admin via PLAIN
             20:21:27: RecordMetadata(topic='sasl-plain-topic', partition=0, topic_partition=TopicPartition(topic='sasl-plain-topic', partition=0), offset=1, timestamp=1744392087197, timestamp_type=0, log_start_offset=0)
             20:21:30: Updating subscribed topics to: frozenset({'sasl-plain-topic'})
             20:21:30: Sending username and password in the clear
             20:21:30: Authenticated as admin via PLAIN
             20:21:30: Sending username and password in the clear
             20:21:30: Authenticated as admin via PLAIN
             20:21:30: Sending username and password in the clear
             20:21:30: Authenticated as admin via PLAIN
             20:21:30: Sending username and password in the clear
             20:21:30: Authenticated as admin via PLAIN
             20:21:30: Discovered coordinator 2 for group custom_metrics_consumer
             20:21:30: Revoking previously assigned partitions set() for group custom_metrics_consumer
             20:21:30: (Re-)joining group custom_metrics_consumer
             20:21:34: Joined group 'custom_metrics_consumer' (generation 12) with member_id aiokafka-0.12.0-0edb9d80-942b-4aa5-9bc1-aeae8f09523b
             20:21:34: Elected group leader -- performing partition assignments using roundrobin
             20:21:34: Successfully synced group custom_metrics_consumer with generation 12
             20:21:34: Setting newly assigned partitions {TopicPartition(topic='sasl-plain-topic', partition=0)} for group custom_metrics_consumer
             20:21:34: KAFKA CONSUMER START
             20:21:34: Sending username and password in the clear
             20:21:34: Authenticated as admin via PLAIN
             20:21:34: KAFKA GET NEW MESSAGE:b'test message'
             20:21:34: LeaveGroup request succeeded
        
        Настройка ACL 
             создание топиков 
                kafka-topics --bootstrap-server localhost:29092 --topic topic-1 --create --partitions 1 --replication-factor 3
                kafka-topics --bootstrap-server localhost:29092 --topic topic-2 --create --partitions 1 --replication-factor 3

                kafka-acls --authorizer-properties zookeeper.connect=zookeeper:2181 --add --allow-principal User:consumer --operation Read --topic topic-1
                kafka-acls --authorizer-properties zookeeper.connect=zookeeper:2181 --add --allow-principal User:consumer --operation Describe --topic topic-1
                kafka-acls --authorizer-properties zookeeper.connect=zookeeper:2181 --add --allow-principal User:producer --operation Write --topic topic-1
                kafka-acls --authorizer-properties zookeeper.connect=zookeeper:2181 --add --allow-principal User:producer --operation Describe --topic topic-1

                kafka-acls --authorizer-properties zookeeper.connect=zookeeper:2181 --add --allow-principal User:consumer --operation Read --topic topic-2
                kafka-acls --authorizer-properties zookeeper.connect=zookeeper:2181 --add --allow-principal User:consumer --operation Describe --topic topic-2
                
             проверим
                sh-4.4$ kafka-acls --authorizer-properties zookeeper.connect=zookeeper:2181 --list
                Warning: support for ACL configuration directly through the authorizer is deprecated and will be removed in a future release. Please use --bootstrap-server instead to set ACLs through the admin client.
                Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=topic-1, patternType=LITERAL)`: 
                  (principal=User:producer, host=*, operation=WRITE, permissionType=ALLOW)
                  (principal=User:producer, host=*, operation=DESCRIBE, permissionType=ALLOW)
                  (principal=User:consumer, host=*, operation=DESCRIBE, permissionType=ALLOW)
                  (principal=User:consumer, host=*, operation=READ, permissionType=ALLOW) 

                 Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=topic-2, patternType=LITERAL)`: 
                  (principal=User:producer, host=*, operation=DESCRIBE, permissionType=ALLOW)
                  (principal=User:producer, host=*, operation=WRITE, permissionType=ALLOW)


Отчет настройка клиента SSL/SASL/ACL 
==================================================================================================================
     python 3.12
     aiokafka==0.12.0
     oc windows (не обязательно - на ней разрабатывалась и тестировалась)

      Установка Python

          python -m venv venv 
          python -m pip install --upgrade pip
       Активания изолированого окружения и установка  библиотек
          venv\scripts\activate.bat (windows)
           source venv/bin/activate
           pip install -r requirements.txt

        Запуск 
            python main.py

        SSL соединеие на /ca   - Сомоподписанный сертификат и ключ

         Пишем под пользователем producer в топик topic-2 и читаем под consumer из topic-2
         результат - Пишем удачно , в чтение - ошибка авторизации
             
            (venv) C:\Users\Andre\Desktop\Архитектура\KAFKA_COURSE\DZ_4_kafka_admin\k_admin\app>python main.py
               10:28:04: Инициализация коннекта - отправка сообщений
               10:28:04: Sending username and password in the clear
               10:28:04: Authenticated as producer via PLAIN
               10:28:04: Sending username and password in the clear
               10:28:04: Authenticated as producer via PLAIN
               10:28:04: Sending username and password in the clear
               10:28:04: Authenticated as producer via PLAIN
               10:28:04: RecordMetadata(topic='topic-2', partition=0, topic_partition=TopicPartition(topic='topic-2', partition=0), offset=3, timestamp=1744442884780, timestamp_type=0, log_start_offset=0)
               10:28:07: Updating subscribed topics to: frozenset({'topic-2'})
               10:28:07: Sending username and password in the clear
               10:28:07: Authenticated as consumer via PLAIN
               10:28:07: Sending username and password in the clear
               10:28:07: Authenticated as consumer via PLAIN
               10:28:07: Sending username and password in the clear
               10:28:07: Authenticated as consumer via PLAIN
               10:28:07: Topic topic-2 is not authorized for this client
               10:28:07: KAFKA ERROR - [Error 29] TopicAuthorizationFailedError: topic-2
               10:28:08: KAFKA CONSUMER START
               10:28:08: KAFKA ERROR -

        

    



   
            
    
     