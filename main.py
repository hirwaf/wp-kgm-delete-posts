import sys
import mysql.connector


def get_arg_value(i):
    try:
        return sys.argv[i]
    except IndexError:
        return None


def default():
    if len(sys.argv) <= 1:
        print("Please provide host user password")
        return 0
    else:
        host = get_arg_value(1)
        user = get_arg_value(2)
        password = get_arg_value(3)
        #
        if host is None:
            print("There is host provided")
            return 0
        if user is None:
            print("There is user provided")
            return 0
        #

        try:
            # Connecting to the mysql DB
            db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database="wp_posts"
            )
            get_posts = db.cursor(dictionary=True)
            sql = """SELECT p.ID FROM wp_kgm.wp_posts as p INNER JOIN wp_kgm.wp_gf_entry as e ON p.ID <> e.post_id
                WHERE p.post_type = 'guestbook_message'
                AND p.post_content LIKE "%http%"
                AND e.created_by is null
                LIMIT 0, 1000;"""
            get_posts.execute(sql)

            posts = get_posts.fetchall()
            print("\nPosts found {}\n".format(len(posts)))
            deleting = db.cursor()
            progress = 0
            for post in posts:
                del_sql = "DELETE FROM wp_kgm.posts WHERE ID={}".format(post.ID)
                deleting.execute(del_sql)
                deleting.commit()
                print((++progress))
            db.close()
        except mysql.connector.Error as e:
            print(str(e))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    default()
