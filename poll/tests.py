import json

from .models import (
    Question,
    Choice,
    Case,
    Stack,
    User,
    Response,
    Result
)

from django.test import TestCase, Client

class QuestionTest(TestCase):
    def setUp(self):
        client = Client()
        Question.objects.create(
            id        = 1,
            question  = "배가 아파서 화장실에 간 당신, 눈앞에 보이는 문고리의 모습",
            image_url = "https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bftest/moon.jpg"
        )

        Stack.objects.create(
            id   = 1,
            name = "Front"
        )

        Stack.objects.create(
            id   = 2,
            name = "Back"
        )

        Choice.objects.create(
            id       = 1,
            choice   = "이게 왜? 잠기기만 하면 된다.",
            question = Question.objects.get(id = 1),
            stack    = Stack.objects.get(id = 2)
        )

        Choice.objects.create(
            id       = 2,
            choice   = "신경 쓰인다.",
            question = Question.objects.get(id = 1),
            stack    = Stack.objects.get(id = 1)
        )

    def tearDown(self):
        Question.objects.all().delete()
        Stack.objects.all().delete()
        Choice.objects.all().delete()

    def test_question_get_success(self):
        client   = Client()
        response = client.get('/poll/question')
        self.assertEqual(response.json(),
            {
                "question_data": [
                    {
                        "id": 1,
                        "question": "배가 아파서 화장실에 간 당신, 눈앞에 보이는 문고리의 모습",
                        "image_url": "https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bftest/moon.jpg",
                        "choice": [
                            {
                                "id": 1,
                                "choice": "이게 왜? 잠기기만 하면 된다."
                            },
                            {
                                "id": 2,
                                "choice": "신경 쓰인다."
                            }
                        ]
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_each_question_get_success(self):
        client   = Client()
        response = client.get('/poll/1')
        self.assertEqual(response.json(),
            {
                "question_data": {
                    "id": 1,
                    "question": "배가 아파서 화장실에 간 당신, 눈앞에 보이는 문고리의 모습",
                    "image_url": "https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bftest/moon.jpg",
                    "choice": [
                        {
                            "id": 1,
                            "choice": "이게 왜? 잠기기만 하면 된다."
                        },
                        {
                            "id": 2,
                            "choice": "신경 쓰인다."
                        }
                    ]
                }
            }
        )
        self.assertEqual(response.status_code, 200)

class ResultTest(TestCase):
    def setUp(self):
        Case.objects.create(
            id   = 1,
            name = "A"
        )

        Stack.objects.create(
            id   = 1,
            name = "Front"
        )

        Stack.objects.create(
            id   = 2,
            name = "Back"
        )

        Question.objects.create(
            id        = 1,
            question  = "배가 아파서 화장실에 간 당신, 눈앞에 보이는 문고리의 모습",
            image_url = "https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bftest/moon.jpg"
        )

        Choice.objects.create(
            id       = 1,
            choice   = "이게 왜? 잠기기만 하면 된다.",
            question = Question.objects.get(id = 1),
            stack    = Stack.objects.get(id = 2)
        )

        Choice.objects.create(
            id       = 2,
            choice   = "신경 쓰인다.",
            question = Question.objects.get(id = 1),
            stack    = Stack.objects.get(id = 1)
        )

        Result.objects.create(
            id = 1,
            name = "기브미 관심 귀여운 답정너 프론트엔드",
            description = "답은 정해져 있어 너는 잘했다고 말만 해. 내가 짠 코드가 화면에 나타났어 자랑하고 싶다 자랑하고 싶어! 우쭈쭈 받고 성장하는 당신은 관종 프론트! 항상 밝고 쾌활한 이미지의 당신은 분위기 메이커! 하지만 속 깊은 고민도 하고 있다는 것을 다른 사람들은 알랑가 몰라~~",
            case = Case.objects.get(id = 1),
            stack = Stack.objects.get(id = 1),
            image_url = "https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bftest/BF_card_1.png"
        )

        Result.objects.create(
            id = 2,
            name = "천사표, 나는 다 좋아요 백엔드",
            description = "이거 예쁘죠! 이거 귀엽죠! 이거 대박이죠!! 옆자리 프론트가 물으면 항상 다 좋아요~ 우리 프론트 하고 싶은 대로 하세요 우쭈쭈~ 언제나 긍정적인 리액션으로 프론트들의 실험대상이 되곤 하는 당신. 소통왕으로 임명합니다! 당신의 긍정 에너지로 백엔드 개발자에 대한 부정적 편견을 다 부숴주세요.",
            case = Case.objects.get(id = 1),
            stack = Stack.objects.get(id = 2),
            image_url = "https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bftest/BF_card_5.png"
        )

    def tearDown(self):
        Case.objects.all().delete()
        Stack.objects.all().delete()
        Question.objects.all().delete()
        Choice.objects.all().delete()
        Result.objects.all().delete()

    def test_result_post_success(self):
        client      = Client()
        result_info = {"answer" : {"1": 2}, "type" : "A"}
        header      = {"HTTP_USER_AGENT" : "browser", "REMOTE_ADDR" : "ip_address"}

        response = self.client.post('/poll/result',
                                    json.dumps(result_info),
                                    **header,
                                    content_type='application/json')

        self.assertEqual(response.json(),
            {
                "result": {
                    "name": "기브미 관심 귀여운 답정너 프론트엔드",
                    "description": "답은 정해져 있어 너는 잘했다고 말만 해. 내가 짠 코드가 화면에 나타났어 자랑하고 싶다 자랑하고 싶어! 우쭈쭈 받고 성장하는 당신은 관종 프론트! 항상 밝고 쾌활한 이미지의 당신은 분위기 메이커! 하지만 속 깊은 고민도 하고 있다는 것을 다른 사람들은 알랑가 몰라~~",
                    "image_url": "https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/bftest/BF_card_1.png",
                    "audio_url": None,
                    "dev_fit": "천사표, 나는 다 좋아요 백엔드"
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_result_post_type_fail(self):
        client      = Client()
        result_info = {"answer" : {"1": 2}}
        header      = {"HTTP_USER_AGENT" : "browser", "REMOTE_ADDR" : "ip_address"}

        response = self.client.post('/poll/result',
                                    json.dumps(result_info),
                                    **header,
                                    content_type='application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_result_post_answer_fail(self):
        client      = Client()
        result_info = {"type" : "A"}
        header      = {"HTTP_USER_AGENT" : "browser", "REMOTE_ADDR" : "ip_address"}

        response = self.client.post('/poll/result',
                                    json.dumps(result_info),
                                    **header,
                                    content_type='application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)
