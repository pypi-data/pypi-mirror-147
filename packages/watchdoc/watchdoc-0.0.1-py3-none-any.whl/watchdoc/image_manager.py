# markdown example for an image in base64 format
# ![Hello World](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEYAAAAUCAAAAAAVAxSkAAABrUlEQVQ4y+3TPUvDQBgH8OdDOGa+oUMgk2MpdHIIgpSUiqC0OKirgxYX8QVFRQRpBRF8KShqLbgIYkUEteCgFVuqUEVxEIkvJFhae3m8S2KbSkcFBw9yHP88+eXucgH8kQZ/jSm4VDaIy9RKCpKac9NKgU4uEJNwhHhK3qvPBVO8rxRWmFXPF+NSM1KVMbwriAMwhDgVcrxeMZm85GR0PhvGJAAmyozJsbsxgNEir4iEjIK0SYqGd8sOR3rJAGN2BCEkOxhxMhpd8Mk0CXtZacxi1hr20mI/rzgnxayoidevcGuHXTC/q6QuYSMt1jC+gBIiMg12v2vb5NlklChiWnhmFZpwvxDGzuUzV8kOg+N8UUvNBp64vy9q3UN7gDXhwWLY2nMC3zRDibfsY7wjEkY79CdMZhrxSqqzxf4ZRPXwzWJirMicDa5KwiPeARygHXKNMQHEy3rMopDR20XNZGbJzUtrwDC/KshlLDWyqdmhxZzCsdYmf2fWZPoxCEDyfIvdtNQH0PRkH6Q51g8rFO3Qzxh2LbItcDCOpmuOsV7ntNaERe3v/lP/zO8yn4N+yNPrekmPAAAAAElFTkSuQmCC)


def image_to_base64(image_file, output_file):

    # need base 64
    import base64
    import sys
    # open the image
    image = open(image_file, 'rb')
    # read it
    image_read = image.read()
    # encode it as base 64
    # after python>=3.9, use `encodebytes` instead of `encodestring`
    image_64_encode = base64.encodestring(image_read) if sys.version_info < (
        3, 9) else base64.encodebytes(image_read)
    # convert the image base 64 to a string
    image_string = str(image_64_encode)
    # replace the newline characters
    image_string = image_string.replace("\\n", "")
    # replace the initial binary
    image_string = image_string.replace("b'", "")
    # replace the final question mark
    image_string = image_string.replace("'", "")
    # add the image tags
    image_string = '<p><img src="data:image/png;base64,' + image_string + '"></p>'
    # write it out
    image_result = open(output_file, 'w')
    image_result.write(image_string)
    
    
if __name__ == "__main__":
    pass
