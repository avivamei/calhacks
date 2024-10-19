BASE_SEARCH = '''Your job is to search for emails from companies that are in direct response to new or in progress job applications. In particular, your focus is {status}. You should use the following notation to filter the results:\nExample filters include from:sender, subject:subject, -filtered_term, in:folder, is:important|read|starred, after:year/mo/date, before:year/mo/date, label:label_name “exact phrase”. Search newer/older than using d (day), m (month), and y (year): newer_than:2d, older_than:1y. Attachments with extension example: filename:pdf. Multiple term matching example: from:amy OR from:david. Set the `max_results` tool argument to {num_results}.'''

NEW_APPLICATIONS = '''You are searching only for emails that are in response to new application submissions. Search for emails in the last year that contain phrases such as "Thank you for your application" or "You've applied" either in the body of the email or the subject line. Do not just use the examples aforementioned but include several permutations of your own that will illicit the most comprehensive search results related to this task.'''