# O.S. Initial Pitching 대본

안녕하세요. 저희는 비트코인 자동매매 프로그램에 대해 initial pitching을 진행할 O.S.조입니다.

저희는 소개및동기, 연구질문, 시스템 구조 설명, 알고리즘, 협업 과정, 메소드, 함의 순으로 발표 진행하도록 하겠습니다.

저희 팀은 주제를 선정함에 있어 네가지 주요 기준을 적용했습니다. 첫째로, 실제로 실행 가능한 주제인지, 둘째,  주어진 기간 안에 프로젝트를 성공적으로 마칠 수 있는지를 평가하였습니다.  또한 셋째, 관련된 오픈소스가 풍부한지, 마지막으로는 저희의 프로젝트가 개인만이 아닌 프로젝트 주제와 관련이 있는 사람들에게 도움을 줄 수 있는지를 고려했습니다.

주식과는 달리 비트코인은 24시간 365일 거래가 가능하여, 거래자들은 비트코인 가격의 끊임없는 변동성으로 인해 지속적으로 시장을 모니터링하고 거래해야 합니다. 이 변동성은 많은 투자자들에게 큰 기회를 제공하면서도, 그에 따른 지속적인 시장 모니터링과 신속한 거래 결정이라는 부담도 안겨줍니다. 뿐만 아니라, 많은 사람들이 비트코인 거래를 시작하지 않는 원인 중 하나가 “어떻게 비트코인을 시작해야 할지 모른다”는 것입니다. 이는 비트코인 시장의 진입 장벽이 여전히 높다는 것을 의미하며, 이러한 장벽을 낮추는 것이 저희 프로젝트의 중요한 동기 중 하나입니다. 

저희 프로젝트는 비트코인 투자와 관련된 지식을 얻기 어려워하는 사람들, 감정적인 판단을 하며 매매하는 사람들을 위해 자동매매 서비스를 제공함으로써 누구나 쉽게 투자를 시작할 수 있도록 돕습니다. 이 서비스(앱)는 투자자들의 감에 의존하지 않고, 전략적으로 투자할 수 있게 도와줄뿐만 아니라, 시간을 절약하고 정신적 피로도를 감소시키는 효과를 제공합니다.

실제로 저희 조원이 비트코인 거래를 직접 해본 경험이 있는데요. 사람이 직접 거래를 할 때 비이성적인 결정을 내리는 경우가 종종 있다고 합니다. 이러한 문제를 해결하기 위해 자동매매 시스템을 도입하면, 투자자는 감정에 휘둘리지 않고 일관된 매매 규칙을 적용할 수 있으며, 이는 투자의 효율성을 극대화하는 동시에 심리적 안정감까지 제공할 것입니다.

저희는 이러한 배경하에 ‘비트코인 자동매매 서비스’를 기획하게 되었고, 이 서비스가 실제로 투자자들에게 매매의 편의성과 수익성을 향상 시킬 수 있는지에 대해 연구하고자 합니다. 이를 기반으로 연구질문을 작성하였습니다.
저희의 연구질문은 ‘비트코인 시장에서 자동매매 알고리즘이 실제로 투자자의 수익성과 편의성을 향상시킬 수 있는가?”입니다. 더 나아가 자동매매 알고리즘을 사용할 때 경험이 많지 않은 투자자들의 수익률에는 어떤 변화가 있는지, 시장 모니터링에 소요되는 시간과 정신적 스트레스를 자동매매 알고리즘이 얼마나 감소시키는지 또한 연구질문으로 선정했습니다.

다음은 저희 시스템 구조 설명입니다.
저희는 사용자가 웹페이지를 통해 Upbit Open API key를 생성하는 방법을 제공하고, access key와 secret key를 입력하는 시스템을 구축할 것입니다. access key와 secret key를 입력받으면, Django의 데이터 베이스로 저장되고, 저장 후, 나중에 사용자에게 자동매매 알고리즘 직접 만들어줄때 변수값로 입력합니다. Upbit Open API키를 통해, 사용자는 자신의 자산을 조회하고, 주문 내역을 확인하고, 실제로 거래 주문을 할 수 있는 기능을 이용할 수 있습니다. 이러한 기능들을 Slack bot과 연동시켜 사용자가 비트코인 자동매매 프로그램을 손쉽게 사용할 수 있도록 할 것입니다. 사용자는 자신의 슬랙 채널에서 매매 관련 알림을 받고, 시스템의 작동 상태를 실시간으로 확인할 수 있습니다. 

오승환 학우가 자동매매 알고리즘에 대해 더 자세하게 설명드리도록 하겠습니다.

---

다음은 자동매매 알고리즘에 관한 내용입니다.

여기서 설명할 알고리즘은 가격이 특정 범위 또는 수준을 '돌파'할 때 매매를 실행하는 돌파매매법으로, 가장 기본적인 알고리즘입니다. 1단계인 데이터 수집과정에서는 pyupbit라이브러리를 사용하여 차트에 대한 7일간의 데이터를 가져옵니다.
이 데이터에는 시가(open), 고가(high), 저가(low), 종가(close) 등의 정보가 포함되어 있습니다.
2단계, 매매 범위 계산에서는 각 일별로 고가와 저가의 차이를 구한 뒤 k값을 곱하여 범위를 계산합니다.
이 때, k는 노이즈의 비율을 뜻합니다. 꾸준한 상승세를 보이면 노이즈가 적으며, 횡보를 하면 노이즈가 많아진다는 의미입니다. 따라서, k의 값이 높으면 매수 목표가를 높게, k값이 낮으면 매수 목표가를 낮게 산정합니다.

3단계 목표가 설정에서는 범위값을 다음 날의 시가에 더해서 목표가를 설정합니다. 고가가 목표가보다 높은 경우 수익율을 계산하고, 그렇지 않은 경우 수익율을 1로 설정합니다.수익률은 종가를 목표가로 나눈 후, 업비트 거래수수료 0.05%를 적용하여 계산합니다.

마지막은 수익률 계산 및 확인입니다. 수익률의 누적 곱을 계산하여 수익률 데이터 프레임의 마지막에서 두 번째 값을 가져옵니다. 두 번째 값을 반환하는 이유는 현재 날짜의 데이터가 아직 종료되지 않았을 수도 있기 때문입니다.

요약하면 매수 목표가와 현재가가 같아지는 순간 **시장가로** **매수**를 진행하며, 오전 9시 **10초** **전에** **해당** **종목을** **모두** **매도**합니다. 오전 9시가 되면 **k의** **값을** **다시** **계산하여** **매수** **목표가를** **다시** **산정**하는 방식입니다. 앞으로 여유가 있다면 이 알고리즘을 보완시키거나 새로운 알고리즘을 추가할 예정입니다.

현재는 매일 정해진 시간에 매도를 해서 하이 리스크 하이 리턴 형식의 매매법인데, 매수가를 기준으로 일정 이상 가격이 떨어지면 바로 매매하는 알고리즘을 추가해 리스크를 줄일 예정입니다.
또한, 앞으로 여유가 있다면 새로운 매매법을 추가할 예정입니다.

다음은 slack 알림 봇에 관한 내용입니다.

우선, 사용자가 slack bot을 생성하고, 토큰을 발급받습니다. 사용자가 웹페이지를 통해 토큰을 입력하면, 서버 데이터베이스에 저장되고, 데이터베이스에 저장된 토큰을 서버내의 프로그램의 변수로 넣어 자동매매 알고리즘과 bot을 연결합니다. 그 후, 설정해둔 정보들을 실시간으로 bot이 알려줍니다. 실시간 자동 알림은 Crontab설정으로 구현합니다. 또한, 사용자가 bot에게 특정 단어를 입력하면, 그에 해당하는 기능을 실행합니다.

구현할 기능으로는

- 시스템 시작/중단
- 현재 프로그램 작동 여부
- 잔고 확인
- 매수목표가, 현재가 확인
- 알고리즘 교체 기능

으로 예정되어 있습니다.

협업과정에서는 github와 notion을 사용할 계획입니다.

개발 단계에서는 GitHub로 각자의 브랜치에서 코드 작업을 시작하고, 기능 개발이나 수정이 완료되면 메인 브랜치로 풀 리퀘스트를 생성하며, 팀원들이 이를 리뷰하고, 피드백을 제공합니다. 또한, 버그 수정이나 기능 개발에 대한 논의를 진행하고, 프로젝트 보드를 사용해 풀 리퀘스트의 상태를 관리합니다. 모든 풀 리퀘스트는 django에서 git을 사용해 수정 내용을 push하여 생성합니다.
Notion으로는 개발 과정에서 업데이트한 사항에 대해 간략히 요약함으로써 진행 과정을 함께 이해합니다. 또한, 회의록을 작성하고, 프로젝트의 진행 상황을 Notion 페이지에 실시간으로 업데이트하여 팀원들과 공유합니다.

리뷰 단계에서는 GitHub로 모든 풀 리퀘스트와 이슈가 해결되었는지 최종적으로 확인하고, Notion으로 프로젝트를 평가하며 개선점과 피드백을 논의합니다. 요약하자면, github로는 코드와 관련된 이슈들을 다루고, notion으로 프로젝트 전반의 흐름을 제어하면서 협업을 진행할 예정입니다.

사용할 오픈소스(메서드)로는 github, upbit API, Slack API, Visual Studio Code등이 있습니다.그 중에서 Github에 업로드된 오픈소스들을 중점적으로 사용할 예정이며, 대표적으로 pyupbit와 같은 여러 라이브러리가 있습니다.

저희 프로젝트의 함의는 비트코인 자동매매 서비스를 배포하는 것입니다. 이 서비스는 코인 투자에 관심은 있지만 경험이 없거나 관련 지식을 쌓는 것이 어려운 사람들을 위한 것입니다. 이들이 손쉽게 자동매매를 통해 투자 경험을 할 수 있도록 돕습니다. 또한, 전략 없이 감에만 의존하여 투자하는 사람들에게도 도움이 됩니다. 이 프로젝트는 시간 절약과 정신적 피로도 감소와 수익성 증가 효과를 가져올 것입니다

감사합니다.