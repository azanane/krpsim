from srcs.Verification import Verification


if __name__=="__main__":
    try:
        verif = Verification()
    except Exception as e:
        print(f'{str(e)}')
        exit(1)