from pyjavaz import JavaObject

point = JavaObject("java.awt.Point", [1, 2])

# access fields
print(point.x, point.y)

# run methods
point.translate(3, 5)
print(point.x, point.y)
