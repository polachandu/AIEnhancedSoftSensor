from SoftSensor.SoftSensor_Admin.Estimator import Estimator


class ValvePressureDropEstimator(Estimator):
    def __init__(self):
        self.Kv = 0.0
        super().__init__()

    def setUp(self):
        self.Kv = 7.0
        return True

    def estimateResults(self, inputs):
        results = inputs
        if len(results) > 0:
            results[0]['S_Pout_kPa'] = results[0]['S_Pin_kPa'] - pow(results[0]['S_F_kgh']/self.Kv, 2)
        return results
