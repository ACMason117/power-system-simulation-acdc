import pytest
from assignment_1.graph_processing import __init__, IDNotUniqueError

class test_id_not_unique():
    def test1(self):
        with pytest.raises(IDNotUniqueError) as excinfo:  
            __init__([1,2,3,4,5], [1,2,3], [(1,2),(2,3),(1,5)], [True, True, True], 1)
        assert str(excinfo.value) == "Vertex IDs are not unique" 

class test_id_not_unique():
    def test1(self):
        with pytest.raises(IDNotUniqueError) as excinfo:  
            __init__([1,2,3,4,5], [3,1,3,2], [(1,2),(2,3),(1,5), (4,5)], [True, True, True], 1)
        assert str(excinfo.value) == "Edge IDs are not unique"
