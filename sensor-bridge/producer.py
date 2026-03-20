import json
from kafka import KafkaProducer

KAFKA_SERVER = 'localhost:9092' # 현재 성공한 IP

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(3, 6, 1)
)

print("입력 대기 중... (종료하려면 'exit' 입력)")

try:
    while True:
        # 사용자로부터 메시지 입력 받기
        msg = input("보낼 메시지 입력: ")
        
        if msg == 'exit':
            break
            
        data = {"status": "SUCCESS", "msg": msg}

        # 메시지 전송
        #producer.send('parking-topic', value=data)
        #producer.flush() # 전송 확정
        #print(f"✅ '{msg}' 전송 완료!")

        # 전송 시 성공 여부를 확인할 수 있도록 callback을 추가하면 더 좋습니다.
        future = producer.send('parking-topic', value=data)
        producer.flush()

        # 실제 전송 결과 확인
        record_metadata = future.get(timeout=10)
        print(f"✅ '{msg}' 전송 완료! (Topic: {record_metadata.topic}, Partition: {record_metadata.partition})")
except Exception as e:
    print(f"전송실패: {e}")
#except KeyboardInterrupt:
#    pass
finally:
    producer.close()
    print("🚀 프로듀서 종료")