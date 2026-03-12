# parkit-infra - Cloud Native Message Pipeline
온프레미스 환경에서의 IaC와 GitOps

"주차가 어려운 초보 운전자를 위한 실시간 코칭 서비스, Park + it의 심장부입니다."
차량 센서 데이터를 100ms 이내로 처리하기 위한 고가용성 및 저지연 메시징 인프라를 구축하고 관리합니다.


## 🏗️ Infrastructure Architecture
본 프로젝트는 K3s 기반 쿠버네티스 환경에서 운영되며, 인프라의 모든 요소는 YAML manifest를 통해 관리됩니다.

- **Cluster**: On-premise K3s (Lightweight Kubernetes)

- **Messaging**: Kafka 3.6.1 (KRaft Mode, Bitnami Image)

- **CD/GitOps**: ArgoCD for automated deployment

- **Network**: Ingress Controller for service exposure & Static ClusterIP for stable internal routing

## 🚀 Key Features
### 1. High Availability Kafka Cluster
- KRaft Mode: ZooKeeper 없이 독립적으로 작동하는 컨트롤러-브로커 통합 클러스터 구축.

- Topic Strategy: 실시간 센서 데이터 수집을 위한 sensor-raw 토픽 최적화.

### 2. Network Stability (Static Endpoint)
- Fixed Infrastructure: 서비스 재배포 시 IP가 휘발되는 문제를 방지하기 위해 ClusterIP를 명시적으로 할당(10.100.100.82).

- Advertised Listeners: K8s 네트워크 내부 도메인 해석 이슈를 해결하기 위해 브로커의 광고 주소를 고정 IP로 매핑.

### 3. GitOps Workflow
- ArgoCD: 모든 인프라 변경 사항을 Git에서 관리하고 자동으로 클러스터에 동기화.

## 🛠️ Critical Troubleshooting (The Saga)
단순 배포를 넘어, 프로젝트 진행 중 마주한 핵심 기술 난제들을 다음과 같이 해결했습니다.

### 🚩 Case 1. OS Library Compatibility (Image Tagging)
- Issue: :latest 이미지 사용 시 내부 스크립트 오류로 인한  `CrashLoopBackOff`.

- Solution: 안정성이 검증된 `3.6.1-debian-11-r0` 태그로 고정하여 런타임 안정성 확보.

### 🚩 Case 2. Metadata Handshake Failure (Advertised Listeners)
- Issue: 클라이언트 접속 시 Connected 상태 이후 데이터 전송 직전 무한 대기(`Metadata timeout`).

- Root Cause: 브로커가 클라이언트에게 전달하는 내부 도메인 주소를 클라이언트가 해석하지 못함.

- Solution: `KAFKA_CFG_ADVERTISED_LISTENERS`를 DNS가 아닌 `Static IP`로 강제 매핑하여 직접 통신 구현.

### 🚩 Case 3. Local DNS Poisoning for Fast Validation
- Issue: 서비스 엔드포인트 해석 오류로 인한 연동 지연.

- Action: 마스터 노드 및 클라이언트의 `/etc/hosts` 파일을 직접 수정하여 도메인-IP 강제 매핑.

- Result: 인프라 전면 수정 전, 이슈의 원인이 DNS 해석 문제임을 단 1분 만에 증명.

## 📂 Repository Structure
```
.
├── k8s-manifests/
│   ├── kafka.yaml      # 최종 Kafka 설정 (Static IP & Advertised Listeners)
│   └── argocd-apps.yaml       # ArgoCD Application 리소스
├── sensor-bridge/             # 인프라 검증용 Pub/Sub 코드
│   ├── producer.py            # Webots 데이터 송신 (Python)
└── README.md
```

## 👥 Authors & Responsibilities
### 김희라 / KimHeera 
- Role: Platform & Infrastructure Lead

- Responsibilities:

    1. Kafka Cluster Engineering: K3s 환경 내 Bitnami Kafka(KRaft) 클러스터 설계 및 구축.

    2. Network Optimization: Advertised Listeners 최적화 및 Static ClusterIP 도입을 통한 통신 가용성 확보.

    3. GitOps Implementation: ArgoCD를 이용한 인프라 배포 자동화 파이프라인 구축.

    4. Infrastructure Troubleshooting: 컨테이너 런타임 오류 및 네트워크 핸드쉐이크 이슈 해결.
### 이예은 / LeeYaeeun
- Role: Data & Simulation Engineer

- Responsibilities:

    1. Webots Simulation: Webots 기반 주차 시뮬레이션 환경 구축 및 차량 센서 모델링.

    2. Data Extraction: 차량 조향각, 속도, 장애물 거리 등 핵심 데이터 추출 로직 개발.

    3. Sensor Bridge Integration: 추출된 시뮬레이션 데이터를 Kafka 프로토콜에 맞춰 전송하는 브릿지 모듈 최적화.
