import json, os, sys, random
def pingtest(output):
                    pingtest = []
                    reply = f"Reply from {output}: bytes=32 time="
                    replyranges = 0
                    timeout = "Request timed out."
                    timeoutranges = replyranges

                    timereg = []
                    #average = 0
                    for y in range(0, 4):
                        choice  = random.choices([reply, timeout])
                        play = f"{random.choices([212, 123, 240, 310, 125, 12, 34, 45, 76, 342])[0]}"
                        times = f"{random.randint(9, 124)}"
                        if choice[0] == timeout:
                            timeoutranges +=1
                        else:
                            replyranges +=1

                        if timeoutranges>2:
                            choice[0] = f"Reply from {output}: bytes=32 time={play}ms TTL={times}"
                            timereg.append(int(play))

                        if choice[0] == reply:
                            choice[0] = choice[0]+f"{play}ms TTL={times}"
                            timereg.append(int(play))
                        pingtest.append(choice[0])
                    total  = 0
                    for numb in timereg:
                        total += numb
                    average = total / len(timereg)
                    Maximum = max(timereg)
                    Minimum = min(timereg)

                    if (replyranges-timeoutranges) == 4:
                        percent = "0%"
                        timeoutrange = 0
                        replyrange = 4
                    elif (replyranges-timeoutranges) == 3:
                        percent = "25"
                        timeoutrange = timeoutranges+1
                        replyrange = replyrange
                    elif (replyranges-timeoutranges) == 2:
                        percent = "50%"
                        timeoutrange = 2
                        replyrange = 2
                    else:
                        percent = "75%"
                        timeoutrange = 3
                        replyrange = 1
                        

                    output =  """Pinging {} with 32 bytes of data:
{}

Ping statistics for {}:
    Packets: Send = 4, Received = {}, Lost = {} ({} loss),
Approximate round trip times in milli-seconds:
    Minimum = {}ms, Maximum = {}ms, Average = {}ms
                                                    """.format(output, "\n".join(pingtest), output, replyrange, timeoutrange, percent, Minimum, Maximum, int(average))
                    return output