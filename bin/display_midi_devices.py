import mido


def main():
    output_names = mido.get_output_names()
    for index, each in enumerate(output_names):
        print('out id: %d name: %s' % (index, each))
    input_names = mido.get_input_names()
    for index, each in enumerate(input_names):
        print('in id: %d name: %s' % (index, each))
if __name__ == '__main__':
    main()