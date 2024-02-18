from datetime import datetime

now = datetime.now()
# Reference:
# format codes of datetime:
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
tplt = """
## %s
- Day: %s, %s 
- Week: %s
- Fullfilling:
- Keywords: 
- Next Week Plan:
""" % (
        now.date(), 
        now.strftime("%a"),
        now.strftime("%p"),
        now.strftime("%W")
        )

