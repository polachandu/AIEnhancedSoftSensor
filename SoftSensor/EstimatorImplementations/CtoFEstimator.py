from SoftSensor.SoftSensor_Admin.Estimator import Estimator


class CtoFEstimator(Estimator):
    def setUp(self):
        return True

    def estimateResults(self, inputs):
        results = inputs
        if len(results) > 0:
            results[0]['T_F'] = results[0]['T_C']*1.8 + 32.0
        return results
