import torch
from torch.utils.data.dataloader import DataLoader

from tests.constants import NUM_DIGITS


def evaluate(model, train_dataset, test_dataset):
    model.eval()
    with torch.no_grad():
        qty_correct_train = _evaluate_dataset(model, train_dataset)
        qty_correct_test = _evaluate_dataset(model, test_dataset)
    model.train()

    return qty_correct_train, qty_correct_test


def _evaluate_dataset(model, dataset):
    factors = torch.tensor([[10 ** i for i in range(NUM_DIGITS + 1)][::-1]]).to('cpu')
    loader = DataLoader(dataset, batch_size=100, num_workers=0, drop_last=False)

    total_correct = 0
    for _, (inputs, _) in enumerate(loader):
        total_correct += _qty_correct(model, inputs.to('cpu'), factors)

    return total_correct


def _qty_correct(model, digits, factors):
    digits_12 = digits[:, :NUM_DIGITS * 2]
    # todo - joel - what does this mean?
    # using greedy argmax, not sampling
    digits_123 = model.generate(digits_12, NUM_DIGITS + 1, do_sample=False)
    digits_3 = digits_123[:, -(NUM_DIGITS + 1):].flip(1)

    digits_1_int = (digits_12[:, :NUM_DIGITS] * factors[:, 1:]).sum(1)
    digits_2_int = (digits_12[:, NUM_DIGITS:NUM_DIGITS * 2] * factors[:, 1:]).sum(1)
    digits_3_prediction = (digits_3 * factors).sum(1)
    digits_3_target = digits_1_int + digits_2_int

    return int((digits_3_prediction == digits_3_target).cpu().sum())