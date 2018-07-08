from proxy_pool_new.scheduler import sheduler


def main():
    s= sheduler()
    s.run()

if __name__=='__main__':
    main()