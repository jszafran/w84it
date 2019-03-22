datasets = {
    'full_valid_data':
        {'name': 'test_product',
         'description': 'Its going to be awesome!',
         'url': 'http://my-product.com',
         'price': 23.5,
         'currency': 'USD',
         'work_start_date': '2018-12-01',
         'launch_date': '2019-05-25'
         },
    'invalid_data_url':
        {'name': 'test_product',
         'description': 'Its going to be awesome!',
         'url': 'http://my pro_duct.com',
         'price': 23.5,
         'currency': 'USD',
         'work_start_date': '2018-12-01',
         'launch_date': '2019-05-25'
         },
    'invalid_data_price_too_many_decimals':
        {'name': 'test_product',
         'description': 'Its going to be awesome!',
         'url': 'http://my-product.com',
         'price': 23.523342,
         'currency': 'USD',
         'work_start_date': '2018-12-01',
         'launch_date': '2019-05-25'
         },
    'invalid_data_price_too_many_digits':
        {'name': 'test_product',
         'description': 'Its going to be awesome!',
         'url': 'http://my-product.com',
         'price': 1234571233223.52,
         'currency': 'USD',
         'work_start_date': '2018-12-01',
         'launch_date': '2019-05-25'
         },
    'invalid_data_price_too_manay_digits_and_decimals':
        {'name': 'test_product',
         'description': 'Its going to be awesome!',
         'url': 'http://my-product.com',
         'price': 1234571233223.52233,
         'currency': 'USD',
         'work_start_date': '2018-12-01',
         'launch_date': '2019-05-25'
         },
    'invalid_data_price_with_no_currency':
        {'name': 'test_product',
         'description': 'Its going to be awesome!',
         'url': 'http://my-product.com',
         'price': 125.99,
         'currency': '-',
         'work_start_date': '2018-12-01',
         'launch_date': '2019-05-25'
         },
    'invalid_data_wrong_dates':
        {'name': 'test_product',
         'description': 'Its going to be awesome!',
         'url': 'http://my-product.com',
         'price': 125.99,
         'currency': '-',
         'work_start_date': '2018-14-01',
         'launch_date': '2019-17-32'
         }
}
