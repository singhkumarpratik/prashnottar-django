import RAKE


def get_topics(text):
    stop_lists = (
        RAKE.SmartStopList()
        + RAKE.FoxStopList()
        + RAKE.NLTKStopList()
        + RAKE.MySQLStopList()
        + RAKE.GoogleSearchStopList()
    )
    Rake = RAKE.Rake(stop_lists)
    topics = [x.title() for x, _ in (Rake.run(text)[:2])]
    print(topics)
    return topics
