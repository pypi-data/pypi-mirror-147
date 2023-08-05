import torch

class InnerProductScorer(torch.nn.Module):
    def forward(self, query, items):
        if query.size(0) == items.size(0):
            if query.dim() < items.dim():
                output = torch.bmm(items, query.view(*query.shape, 1))
                output = output.view(output.shape[:-1])
            else:
                output = torch.sum(query * items, dim=-1)
        else:
            output = torch.matmul(query, items.T)
        return output

class CosineScorer(InnerProductScorer):
    def forward(self, query, items):
        output = super().forward(query, items)
        output /= torch.norm(items, dim=-1)
        output /= torch.norm(query, dim=-1, keepdim=(query.dim()!=items.dim() or query.size(0)!=items.size(0)))
        return output


class EuclideanScorer(InnerProductScorer):
    def forward(self, query, items):
        output = -2 * super().forward(query, items)
        output += torch.sum(torch.square(items), dim=-1)
        output += torch.sum(torch.square(query), dim=-1, keepdim=(query.dim()!=items.dim() or query.size(0)!=items.size(0)))
        return -output
        

class MLPScorer(InnerProductScorer):
    def __init__(self, transform):
        super().__init__()
        self.trans = transform

    def forward(self, query, items):
        if query.size(0) == items.size(0):
            if query.dim() < items.dim():
                input = torch.cat((query.unsqueeze(1).repeat(1, items.shape[1], 1), items), dim=-1)
            else:
                input = torch.cat((query, items), dim=-1)
        else:
            query = query.unsqueeze(1).repeat(1, items.size(0), 1)
            items = items.expand(query.size(0), -1, -1)
            input = torch.cat((query, items), dim=-1)
        return self.trans(input).squeeze(-1)

class NormScorer(InnerProductScorer):
    def __init__(self, p=2):
        super().__init__()
        self.p = p

    def forward(self, query, items):
        # ([batch_size, dim], [batch_size, neg, dim]) or ([num_users, dim], [num_items, dim])
        if query.dim() < items.dim() or query.size(0) != items.size(0):
            query.unsqueeze_(1)
        output = torch.norm(query - items, p=self.p, dim=-1)
        return -output
