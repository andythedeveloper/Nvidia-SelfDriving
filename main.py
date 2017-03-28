import load_data
from model import NVIDA
import time

from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

print('Loading data...')
train_x, train_y, test_x, test_y = load_data.return_data()


print('Loading model')
nvidia = NVIDA()

checkpointer = ModelCheckpoint(
    filepath="{epoch:02d}-{val_loss:.12f}.hdf5",
    verbose=1,
    save_best_only=True
)

lr_plateau = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5, min_lr=0.000001)

epochs = 100
batch_size = 128

print('Starting training')
history = nvidia.fit(train_x, train_y,
    validation_data=(test_x, test_y),
    nb_epoch=epochs,
    batch_size=batch_size,
    callbacks=[checkpointer, lr_plateau]
)

with open('history_{}.json'.format(time.time()), 'wb') as fp:
    # dict with np array as items are not serializable
    json.dump(dict((k, np.array(v).tolist()) for k, v in history.history.items()), fp)
print('Done')
