from django.test import TestCase


# Create your tests here.

class IDCTest(TestCase):
    def test_list(self):
        response = self.client.get('/base/idc/')
        self.assertEqual(response.status_code, 200)
        res = response.json()
        print("res", res)
        self.assertEqual(res.get('code'), 200, )

    def test_insert(self):
        data = {"Name": "baidu", "Idc": "百度", "Remark": "测试数据"}
        response = self.client.post('/base/idc/', data=data)
        res = response.json()
        print("in", res)
        self.assertEqual(res.get('code'), 200, )

    def test_update(self):
        data = {"Name": "baidu2"}
        response = self.client.put('/base/idc/1/', data=data, content_type="application/json")
        res = response.json()
        self.assertEqual(res.get('code'), 200, )

    def test_detail(self):
        response = self.client.delete('/base/idc/1/')
        res = response.json()
        self.assertEqual(res.get('code'), 200, )


class ENVTest(TestCase):
    def test_list(self):
        response = self.client.get('/base/env/')
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res.get('code'), 200, )

    def test_insert(self):
        data = {"Name": "测试", "Code": "test", "Priority": 10}
        response = self.client.post('/base/env/', data=data)
        res = response.json()
        self.assertEqual(res.get('code'), 200, )

    def test_update(self):
        self.test_insert()
        data = {"Name": "baidu2"}
        response = self.client.put('/base/env/1/', data=data, content_type="application/json")
        res = response.json()
        self.assertEqual(res.get('code'), 200, )

    def test_detail(self):
        self.test_insert()
        response = self.client.delete('/base/env/1/')
        res = response.json()
        self.assertEqual(res.get('code'), 200, )


class RegionTest(TestCase):
    def test_list(self):
        response = self.client.get('/base/env/')
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res.get('code'), 200, )

    def test_insert(self):
        data = {"Name": "测试", "Code": "test", "Priority": 10}
        response = self.client.post('/base/env/', data=data)
        res = response.json()
        self.assertEqual(res.get('code'), 200, )

    def test_update(self):
        self.test_insert()
        data = {"Name": "baidu2"}
        response = self.client.put('/base/env/1/', data=data, content_type="application/json")
        res = response.json()
        self.assertEqual(res.get('code'), 200, )

    def test_detail(self):
        self.test_insert()
        response = self.client.delete('/base/env/1/')
        res = response.json()
        self.assertEqual(res.get('code'), 200, )
