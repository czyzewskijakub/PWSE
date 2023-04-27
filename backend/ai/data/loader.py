from backend.ai.PrepareData import PrepareData
from backend.ai.VideoViewsPredictor import VideoViewsPredictor
from backend.ai.VideoViewsPredictorTrainer import VideoViewsPredictorTrainer

if __name__ == "__main__":
    epochs = 900000
    path = f'{epochs}.pt'
    data = PrepareData('data/data.csv')
    print(data.DfFinal.columns)
    net = VideoViewsPredictor(data.Columns)

    trainer = VideoViewsPredictorTrainer(net)
    # trainer.train(data.X_train, data.Y_train, epochs)
    # trainer.evaluate(data.X_test, data.Y_test)
    # trainer.save(path)
    trainer.load(path)
    # trainer.quick_predict(data.X_test, data.Y_test, 10)
    # print(data.X_test[0])
    # print(data.Y_test[0])
    print(trainer.compute_accuracy(data.X_test, data.Y_test, 10))
