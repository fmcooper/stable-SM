
# Used by the python statistics program to collect results for each experiment together
# @author Frances

class experiment:
    numRotations = -1
    numStableMatchings = -1
    egalCost = -1
    seCost = -1
    RMprofile = []
    RMegalCost = -1
    RMseCost = -1
    GENprofile = []
    GENegalCost = -1
    GENseCost = -1
    GMprofile = []
    GMegalCost = -1
    GMseCost = -1
    Duration_ModCreation_ms = -1
    Duration_GetSolution_ms = -1
    Duration_CollectRes_ms = -1
    global Duration_Total_ms
    global Duration_Total_ms_GSNS
    global Duration_Total_ms_GSS
    Duration_Total_ms = -1
    Duration_Total_ms_GSNS = -1
    Duration_Total_ms_GSS = -1



    # each of the three algorithms is recorded separately
    # this function tests whether the overall time taken is beyond a given timeout time
    def timeout(self, timeout):
        if self.Duration_Total_ms + self.Duration_Total_ms_GSNS + self.Duration_Total_ms_GSS < timeout:
            return False
        else:
            return True

