import numpy as np

from triton_bert.triton_bert import TritonBert

"""
30.171.160.44
/nfsc/zhizhe_bear_id116135_vol1001_dev/liutaichen992/shared_data/chinese_L-12_H-768_A-12

"""

# 金服催收的坐席施压点/政策 意图识别
AGENT_INTENTIONS = ['减免政策', '分期政策', '底线政策', '怀柔策略', '征信施压', '风险施压', '法诉施压', '降额', '一次性结清', '三方施压', '停卡警示', '上门催收', '资产冻结', '其他']
# 客户不还款原因 意图识别
CUSTOMER_INTENTIONS = ['资金困难', '无偿还能力', '拖延时间', '今天晚点', '质疑逾期', '看看尽量', '忘记处理', '忙碌未处理', '地理位置不便', '其他', '不可以其他', '曾无电话联系', '钱到就还', '非本人还款', '金额来由', '近期还款', '卡片限额', '稍后处理', '他人用卡', '已还部分', '已还款', '异常情况', '自动扣款', '还两期全款']
class IntentionClassification(TritonBert):
    INTENTIONS = None
    def proprocess(self, triton_output):

        return [self.INTENTIONS[np.argmax(x)] for x in triton_output[0]]


if __name__ == "__main__":
    # model = IntentionClassification(triton_host="30.171.160.44", model="agent_intention_classification", vocab="./vocab/bert_agent_intention_classification")
    # IntentionClassification.INTENTIONS = AGENT_INTENTIONS
    # ret = model(["你的情况符合减免政策", "你的条件符合分期政策"])
    # print(ret)

    model = IntentionClassification(triton_host="30.171.160.44", model="customer_intention_classification", vocab="./vocab/bert_customer_intention_classification")
    IntentionClassification.INTENTIONS = CUSTOMER_INTENTIONS
    #use for batch inference
    ret = model(["我的钱都用来喝咖啡了，没钱了", "今天晚点，我还在外面哈"])
    print(ret)