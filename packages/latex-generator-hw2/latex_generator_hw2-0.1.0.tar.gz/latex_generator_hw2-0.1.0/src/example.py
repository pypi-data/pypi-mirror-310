from latex_generator import generate_table, generate_image

if __name__ == "__main__":
    data = [["asdasdasdasdasdasdA", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
    latex_table = generate_table(data)
    print(latex_table)

    latex_image = generate_image("image.jpg", "Sample Image", "fig:sample")
    print(latex_image)
