from recstudio.model import basemodel, loss_func, scorer
from recstudio.ann import sampler
from recstudio.data import advance_dataset
import torch

class CML(basemodel.TwoTowerRecommender):
    def build_user_encoder(self, train_data):
        return torch.nn.Embedding(train_data.num_users, self.embed_dim, padding_idx=0)

    def get_dataset_class(self):
        return advance_dataset.ALSDataset

    def config_scorer(self):
        return scorer.EuclideanScorer()

    def build_sampler(self, train_data):
        return sampler.UniformSampler(train_data.num_items-1, self.score_func)

    def config_loss(self):
        class CMLoss(loss_func.PairwiseLoss):
            def __init__(self, margin=2, num_items=None):
                super().__init__()
                self.margin = margin
                self.n_items = num_items

            def forward(self, label, pos_score, log_pos_prob, neg_score, neg_prob):
                pos_score[pos_score == -float("inf")] = float("inf")
                loss = torch.max(torch.max(neg_score, dim=-1).values.unsqueeze(-1) - pos_score + self.margin, pos_score.new_zeros(pos_score.size(1)))
                if self.n_items is not None:
                    impostors = neg_score.unsqueeze(1) - pos_score.unsqueeze(-1) + self.margin > 0
                    rank = torch.mean(impostors.to(torch.float32), -1) * self.n_items
                    return torch.mean(loss * torch.log(rank + 1))
                else:
                    return torch.mean(loss)
        return CMLoss(self.config['margin'], self.config['use_rank_weight'])