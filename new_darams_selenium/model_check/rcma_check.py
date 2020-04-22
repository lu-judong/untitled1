import math


class rcma:
    def check(self,beta,eta,any,timeRange):
        L = []

        avg = timeRange / 10
        for i in range(1,11):
            L.append(round(avg * i,4))
        print(L)
        # 失效率
        failureRates = []
        # 可靠度
        reliabilitys = []
        # 故障概率
        failureProbabilitys = []
        # 概率密度
        probabilityDensitys = []
        for i in L:
            if beta == 1:
                failureRate = (1 / eta) * 1000000
            else:
                failureRate = (beta / eta) * math.pow(i / eta, beta - 1) * 1000000

            failureRates.append(failureRate)
            reliability = 1 / math.pow(math.e, math.pow(i / eta, beta))
            reliabilitys.append(reliability)

            failureProbability = 1 - reliability
            failureProbabilitys.append(failureProbability)

            probabilityDensity = (failureRate / 1000000) * reliability
            probabilityDensitys.append(probabilityDensity)
        print(failureRates)
        print(reliabilitys)
        print(failureProbabilitys)
        print(probabilityDensitys)
rcma().check(0.3,0.2,3,200)