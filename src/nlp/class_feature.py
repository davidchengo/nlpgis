class FeatureSet:
    def __init__(self, quorum):
        self.quorum=quorum
        self.vote_sum=0
        self.features= []
        self.feature_used_flg=[]
    def add_feature(self,features):     # features is a list
        self.features.append(features)
        self.feature_used_flg.append(False)
    def isFeatureQuorumMet(self,token,tmp_dump_lst):
        for i in xrange(len(self.features)):
            if self.feature_used_flg[i]==False:
                if token in self.features[i].lst:
                    self.vote_sum+=self.features[i].votes
                    self.feature_used_flg[i]=True
                    tmp_dump_lst.append("Feature found: %s. Quorum update %d/%d\n" % (token,self.vote_sum,self.quorum))
                    if self.vote_sum>=self.quorum:
                        tmp_dump_lst.append("Feature quorum satisfied. vote_sum %d >= quorum %d\n" % (self.vote_sum,self.quorum))
                        return True
                    
        return False
    def reset(self):
        for i in xrange(len(self.feature_used_flg)):
            self.feature_used_flg[i]=False
        self.vote_sum=0
            
class Feature:
    def __init__(self, lst, votes):
        self.lst= lst
        self.votes= votes