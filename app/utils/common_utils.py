
def calculate_relevance(blog, user_tags):
    # Count the number of tags in the blog that are also in the user's liked tags
    common_tags_count = len(set(blog['tags']).intersection(user_tags))

    # You can refine this logic. For example, use weighted scores for different tags
    return common_tags_count
