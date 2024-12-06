from o3seespy.base_model import OpenSeesObject


class AlgorithmBase(OpenSeesObject):
    op_base_type = "algorithm"

    def to_process(self, osi):
        if osi is None:
            return
        OpenSeesObject.to_process(self, osi)

    def reapply(self, osi):
        self.to_process(osi)


class Linear(AlgorithmBase):
    op_type = "Linear"

    def __init__(self, osi, secant=False, initial=False, factor_once=False):
        self.osi = osi
        self.secant = secant
        self.initial = initial
        self.factor_once = factor_once
        self._parameters = [self.op_type, self.secant, self.initial, self.factor_once]
        self.to_process(osi)


class Newton(AlgorithmBase):
    op_type = "Newton"

    def __init__(self, osi, secant=False, initial=False, initial_then_current=False):
        self.osi = osi
        self.secant = secant
        self.initial = initial
        self.initial_then_current = initial_then_current
        self._parameters = [self.op_type, self.secant, self.initial, self.initial_then_current]
        self.to_process(osi)


class SecantNewton(AlgorithmBase):
    op_type = "SecantNewton"

    def __init__(self, osi, iterate='current', increment='current', maxDim=3):
        self.osi = osi
        self.iterate = iterate
        self.increment = increment
        self.maxDim = maxDim
        self._parameters = [self.op_type, self.iterate, self.increment, self.maxDim]
        self.to_process(osi)


class RaphsonNewton(AlgorithmBase):
    op_type = "RaphsonNewton"

    def __init__(self, osi, iterate='current', increment='current'):
        self.osi = osi
        self.iterate = iterate
        self.increment = increment
        self._parameters = [self.op_type, self.iterate, self.increment]
        self.to_process(osi)


class KrylovNewton(AlgorithmBase):
    op_type = "KrylovNewton"

    def __init__(self, osi, tang_inter='current', tang_incr='current', max_inter=3):
        """

        Parameters
        ----------
        osi
        tang_inter: str
            options are: 'current', 'initial', 'noTangent'
        tang_incr
        max_inter
        """
        self.osi = osi
        self.tang_inter = tang_inter
        self.tang_incr = tang_incr
        self.max_inter = max_inter
        self._parameters = [self.op_type, self.tang_inter, self.tang_incr, self.max_inter]
        self.to_process(osi)


class ModifiedNewton(AlgorithmBase):
    op_type = "ModifiedNewton"

    def __init__(self, osi, secant=False, initial=False):
        """

        Parameters
        ----------
        osi
        secant: bool
            Flag to indicate to use secant stiffness.
        initial: bool
            Flag to indicate to use initial stiffness
        max_inter
        """
        self.osi = osi
        self.secant = secant
        self.initial = initial
        self._parameters = [self.op_type, self.secant, self.initial]
        self.to_process(osi)


class NewtonLineSearch(AlgorithmBase):
    op_type = 'NewtonLineSearch'

    def __init__(self, osi, search_type=None, tol=None, max_iter=None, min_eta=None, max_eta=None):
        """
        
        :param osi: 
        :param search_type: str 
        :param tol: default 0.8
        :param max_iter: default=10
        :param min_eta: deault=0.1
        :param max_eta: default=10
        """
        self.osi = osi
        if search_type is None:
            self.search_type = None
            self._parameters = [self.op_type, search_type]
        else:
            self.search_type = search_type
            self._parameters = [self.op_type, search_type]
        
        if tol is not None:
            self._parameters += ['-tol', tol]
        if max_iter is not None:
            self._parameters += ['-maxIter', max_iter]
        if min_eta is not None:
            self._parameters += ['-minEta', min_eta]
        if max_eta is not None:
            self._parameters += ['-maxEta', max_eta]
        self.to_process(osi)


class Broyden(AlgorithmBase):
    op_type = 'Broyden'

    def __init__(self, osi, secant=False, initial=False, count=10):
        self.osi = osi
        self._parameters = [self.op_type, secant, initial, count]
        self.to_process(osi)

class BFGS(AlgorithmBase):
    op_type = 'BFGS'

    def __init__(self, osi, secant=False, initial=False, count=10):
        self.osi = osi
        self._parameters = [self.op_type, secant, initial, count]
        self.to_process(osi)