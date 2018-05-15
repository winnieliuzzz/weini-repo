import database
from models.post import Post


database.Database.initialize()

blog = Blog(author="Weini",
            title="sample title",
            description="Sample description")

blog.new_post()

blog.save_to_mongo()

Blog.from_mongo()

blog.get_posts()