def say_hello():
    print("Hello!")


def run_with_announce(func):
    print("Running the function...")
    func()
    print("Function has finished running.")


print("Calling say_hello directly:")
say_hello()

print()
print("Calling say_hello with run_with_announce:")
run_with_announce(say_hello)


def gift_wrap(func):
    def wrapper():
        print("🎁 Wrapping the function with a gift box! 🎁")
        func()
        print("🎁 The gift box is now open! 🎁")

    return wrapper


def say_hello():
    print("Hello!")


say_hello = gift_wrap(say_hello)

say_hello()

print("--------------------")


@gift_wrap
def say_hello():
    print("Hello!")


say_hello()

print()
print(">>>connecting to discord bot:")
print("@bot.event就是這個用法")
print(">>>discord 幫你定義好  bot.event 裝飾詞")
print(">>>當你在函數上使用 @bot.event 時，discord 就知道這是一個事件處理器")
print("----------------------------")


def register_command(name, description):
    print(f"[登記] 指令/{name} - {description}")

    def decorator(func):
        def wrapper():
            print(f"執行指令: /{name}")
            func()

        return wrapper

    return decorator


register_command(name="hello", description="打招呼的指令")


def hello_command():
    print("Hello, this is the /hello command!")


hello_command()
print("----------------------------")
