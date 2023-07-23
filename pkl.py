import pickle
import numpy as np


# a = np.array([[30., 480.], [560., 480.], [140., 320.], [450., 320.]], dtype=np.float32)
a = np.array([[180., 310.], [450., 310.], [557., 480.], [70., 480.]], dtype=np.float32)
b = np.array([[160., 310.], [480., 310.], [607., 480.], [30., 480.]], dtype=np.float32)
c = np.array([[226., 316.], [408., 313.], [501., 476.], [155., 476.]], dtype=np.float32)
d = np.array([[215., 316.], [350., 313.], [450., 476.], [155., 476.]], dtype=np.float32)
to_save = {'pts_src': a}
to_save_b = {'pts_src': b}
to_save_c = {'pts_src': c}
to_save_d = {'pts_src': d}
# a = [[238., 316.], [402., 313.], [501., 476.], [155., 476.]]

with open('test_c.pkl', 'wb') as f:
    pickle.dump(to_save_c, f)

with open('test_c.pkl', 'rb') as f:
    b = pickle.load(f)

print(b)

with open('./perspect_param.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)