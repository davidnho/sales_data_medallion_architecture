from prefect import flow,task

@flow
def saySomething():
    print("Hello world!")
    
saySomething()