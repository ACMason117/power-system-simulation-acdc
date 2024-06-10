# node
    node = initialize_array('input', 'node', 10)
    node['id'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    node['u_rated'] = [10500, 400, 400, 400, 400, 400, 400, 400, 400, 400]
    # line
    line = initialize_array('input', 'line', 9)
    line['id'] = [16, 17, 18, 19, 20, 21, 22, 23, 24]
    line['from_node'] = [1, 2, 2, 4, 1, 6, 6, 8, 4]
    line['to_node'] = [2, 3, 4, 5, 6, 7, 8, 9, 8]
    line['from_status'] = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    line['to_status'] = [1, 1, 1, 1, 1, 1, 1, 1, 0]
    line['r1'] = [0.0003099357220775627,5.157537412993188e-05,0.0003301670269508862,5.630462672605844e-05,0.0003164960265303119,5.187185585567009e-05,0.0003094577950524227,6.153692945664266e-05,0.0003603813916769252]
    line['x1'] = [0.0001406945054167883,7.174018206043156e-06,]
    line['c1'] = [1.406945054167883e-055, 5.235094366572033e-07,]
    line['tan1'] = [0.003,0.003,0.003,0.003,0.003,0.003,0.003,0.003,0.003,]
    line['r0']=[0.001121477941728023,0.0001745031455524011,]
    line['x0']=[0.0003874196525969534,2.03587003144468e-05,]
    line['c0']=[8.360108292881625e-06,3.102278143153798e-07,]
    line['tan0']=[0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,]
    line['i_n'] = [4485911.766912092,96946.19197355618]
    # load
    sym_load = initialize_array('input', 'sym_load', 4)
    sym_load['id'] = [12, 13, 14, 15]
    sym_load['node'] = [3, 5, 7, 9]
    sym_load['status'] = [1, 1, 1, 1]
    sym_load['type'] = [0, 0, 0, 0]
    sym_load['p_specified'] = [0, 0, 0, 0]
    sym_load['q_specified'] = [0, 0, 0, 0]
    # source
    source = initialize_array('input', 'source', 1)
    source['id'] = [10]
    source['node'] = [0]
    source['status'] = [1]
    source['u_ref'] = [1.05]
    source['sk']=[200000000]
    #transformer
    transformer=initialize_array('input', 'transformer', 1)
    transformer["id"] = [11]
    transformer["from_node"] = [0]
    transformer["to_node"] = [1]
    transformer["from_status"] = [1]
    transformer["to_status"] = [1]
    transformer["u1"] = [10750]
    transformer["u2"] = [420]
    transformer["sn"] = [630000]
    transformer["uk"] = [0.041]
    transformer["pk"] = [5200]
    transformer["i0"] = [0.01]
    transformer["p0"] = [745]
    transformer["winding_from"] = [2]
    transformer["winding_to"] = [1]
    transformer["clock"] = [5]
    transformer["tap_side"] = [0]
    transformer["tap_pos"] = [3]
    transformer["tap_min"] = [5]
    transformer["tap_max"] = [1]
    transformer["tap_nom"] = [3]
    transformer["tap_size"] = [250]
    transformer["r_grounding_to"] = [0]
    transformer["x_grounding_to"] = [0]

    # all
    input_data = {
        'node': node,
        'line': line,
        'sym_load': sym_load,
        'source': source,
        'transformer': transformer
    }
