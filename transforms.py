# Allows you to switch between the two types of transformations
def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)
    
# Transform in 2D    
def transform_2D(self, x, y):
    return int(x), int(y)

# Transform in perspective
def transform_perspective(self, x, y):
    lin_y = self.perspective_point_y * y / self.height
    if lin_y > self.perspective_point_y:
        lin_y = self.perspective_point_y
    
    diff_y = self.perspective_point_y - lin_y
    diff_x = x - self.perspective_point_x
    
    factor_y = diff_y / self.perspective_point_y
    factor_y = pow(factor_y, 4)  # multiplies the value squared

    offset_x = diff_x * factor_y

    tr_x = self.perspective_point_x + offset_x
    tr_y = self.perspective_point_y - factor_y * self.perspective_point_y

    return int(tr_x), int(tr_y)