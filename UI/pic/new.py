def geturl(path):
    import cloudinary
    import cloudinary.uploader

    cloudinary.config( 
    cloud_name = "dcfcqjyxs", 
    api_key = "893987629983942", 
    api_secret = "m4QRWqgXpYTkXeQfeQ8dJCEVkig"
    )

    a = cloudinary.uploader.upload(path)

    print(a["secure_url"])
    return a["secure_url"]