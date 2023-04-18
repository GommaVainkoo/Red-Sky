def transform(self, x, y):
    #return self.transform_2D(x,y)
    return self.transform_prespective(x, y)


def transform_2D(self, x, y):
    return int(x), int(y)

def transform_prespective(self, x, y):
    trans_y = y * self.y_cor / self.height
    if trans_y > self.y_cor:
        trans_y = self.y_cor
    diff_x = x - self.x_cor
    diff_y = self.y_cor - trans_y
    factor_X = diff_y/self.y_cor
    factor_X=pow(factor_X,4)
    trans_x = self.x_cor + diff_x * factor_X
    trans_y=self.y_cor-factor_X*self.y_cor
    return int(trans_x), int(trans_y)
