  SonyAlarmLog.joins(:sony_alarm_test)
    .where{ name =~ event_name }
    .where{ utc_time.gt (my{utc_time} + TIME_CORRECTION) }
    .where(sony_alarm_tests: {ip: sony_alarm_test.ip})
    .where(sony_alarm_tests: {round: sony_alarm_test.round})
    .where(sony_alarm_tests: {firmware_version: sony_alarm_test.firmware_version})
