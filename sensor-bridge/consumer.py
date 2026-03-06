import json
from kafka import KafkaConsumer

# [수정] 고정 IP 사용
KAFKA_SERVER = '10.100.100.82:9092'

consumer = KafkaConsumer(
    'parking-topic',
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest', 
    enable_auto_commit=True,
    group_id='debug-group-final-1', # [팁] 그룹ID를 새걸로 바꿔야 이전 메시지부터 다 나옵니다.
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    api_version=(3, 6, 1) # [수정] 실제 버전 3.6.1
)

print(f"👂 [Consumer] {KAFKA_SERVER}에서 메시지를 기다립니다...")

try:
    for message in consumer:
        print(f"📩 [수신성공] {message.offset}번 데이터: {message.value}")
except Exception as e:
    print(f"❌ 오류 발생: {e}")
finally:
    consumer.close()