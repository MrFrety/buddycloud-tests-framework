from visibility_utils import performVisibilityTests

def testFunction(domain_url, session):

	expected_results = {
		'ALL_METADATA_ACCESS'	: { True : ["test_user_channel_open@" + domain_url, "test_topic_channel_open@topics." + domain_url] },
		'MOOD_STATUS_ACCESS'	: { True : ["test_user_channel_open@" + domain_url] },
		'POSTS_READ_ACCESS'	: { True : ["test_user_channel_open@" + domain_url, "test_topic_channel_open@topics." + domain_url] },
		'SUBSCRIBERS_ACCESS'	: { True : ["test_user_channel_open@" + domain_url, "test_topic_channel_open@topics." + domain_url] },
		'BANNED_SUBSCRIBERS_ACCESS' : { True : ["test_user_channel_open@" + domain_url] }
#		'SUBSCRIBED_TO_ACCESS'	: { True : ["test_user_channel_open@" + domain_url] },
#		'GEOLOC_ACCESS'		: { True : ["test_user_channel_open@" + domain_url] }
	}

	(status, partial_report) = performVisibilityTests(session, domain_url, "test_user_channel_open", expected_results)

	if status == 0:
		briefing = "Visibility tests for <strong>test_user_channel_open@%s</strong> were successful!" % domain_url
	else:
		briefing = "Visibility tests for <strong>test_user_channel_open@%s</strong> were not entirely successful!" % domain_url

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
