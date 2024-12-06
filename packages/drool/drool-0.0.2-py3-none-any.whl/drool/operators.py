operators = dict(
                greater_than =lambda context, value: context > value,
    greater_than_or_equal_to =lambda context, value: context >= value,
                   less_than =lambda context, value: context < value,
       less_than_or_equal_to =lambda context, value: context <= value,
                    equal_to =lambda context, value: context == value,
                not_equal_to =lambda context, value: context != value,
                    contains =lambda context, value: value in context,
                        isin =lambda context, value: context in value,
                    not_null =lambda context, _: context != None,
                        true =lambda context, _: context == True,
                       false =lambda context, _: context == False,
)