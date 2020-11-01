class NaiiveBaye:
    def __init__(self,Attribute,DataInstance):
        self.Attribute = Attribute
        self.DataInstance = DataInstance
        self.classAmount = len(Attribute)
        self.dataAmount = len(DataInstance)
        self.dataDomain,self.Datacolumn = self.find_DomainEach_attribute()
        self.NumberOfEachData = self.find_NumberOfEach_DataDomain()

    def find_DomainEach_attribute(self):
        result = []
        datacolumn = []
        for A in range(0,self.classAmount):
            each_att = []
            each_att_DC = []
            for D in self.DataInstance:
                each_att_DC.append(D[A])
                if D[A] not in each_att:
                    each_att.append(D[A])
            result.append(each_att)
            datacolumn.append(each_att_DC)
        return result,datacolumn

    def find_NumberOfEach_DataDomain(self):
        result = []
        for i,DD in enumerate(self.dataDomain):
            each_att = []
            for D in DD:
                cout = self.Datacolumn[i].count(D)
                each_att.append(cout)
            result.append(each_att)
        return result
    def condition_prob(self,x_attribute,y_attribute,x,y):
        num = 0
        ix = self.Attribute.index(x_attribute)
        iy = self.Attribute.index(y_attribute)
        id_y = self.Datacolumn[iy].count(y)
        for DT in self.DataInstance:
            if DT[ix] == x and DT[iy] == y:
                num += 1
        if id_y != 0:
            if num == 0:
                return 1/(id_y+len(self.dataDomain[id_y]))
            return num/id_y
        else:
            return 0

    def condition_prob_full(self,instance,y_attribute):
        iy = self.Attribute.index(y_attribute)
        op = 1
        for i,data in enumerate(instance):
            if i != iy:
                attibute = self.Attribute[i]
                o = self.condition_prob(attibute,y_attribute,data,instance[iy])
                op *= o
        return op

    def compair_prob(self,chosen_instance,y_attribute):
        iy = self.Attribute.index(y_attribute)
        instance_result = []
        result = {}
        for id_y in self.dataDomain[iy]:
            each_result = []
            for c,att in enumerate(self.Attribute):
                if c != iy:
                    each_result.append(chosen_instance[att])
                else:
                    each_result.append(id_y)
            instance_result.append(each_result)
        for k,each_instance in enumerate(instance_result):
            result.update({self.dataDomain[iy][k]:self.condition_prob_full(each_instance,y_attribute)*(self.NumberOfEachData[iy][k]/self.dataAmount)})
        return result
        
    def create_chosen_Dict(self,y_attribute):
        result = {}
        iy = self.Attribute.index(y_attribute)
        for i,each in enumerate(self.Attribute):
            if i != iy:
                result.update({each:self.dataDomain[i]})
        return result

    def create_chosen_attribute(self,y_attribute):
        result = []
        iy = self.Attribute.index(y_attribute)
        for i,each in enumerate(self.Attribute):
            if i != iy:
                result.append(each)
        return result

    def find_best_result(self,result):
        best = ""
        mid = 0
        for r in result:
            if result[r] > mid:
                mid = result[r]
                best = r
            elif result[r] == mid:
                mid = result[r]
                best = best + " And " + r
        return best
    
             