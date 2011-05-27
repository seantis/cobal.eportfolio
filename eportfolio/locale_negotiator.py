from repoze.bfg.settings import get_settings

def get_preferred_languages(request):
    
    if "set_language" in request.GET:
        return [ request.GET['set_language'] ]
    
    # Not availabe in DummyRequest during testing
    if not hasattr(request, 'accept_language') or not hasattr(request.accept_language, 'header_value'):
        return []
    
    accept_langs = request.accept_language.header_value.split(',')

    # Normalize lang strings
    accept_langs = [normalize_lang(l) for l in accept_langs]
    # Then filter out empty ones
    accept_langs = [l for l in accept_langs if l]

    accepts = []
    for index, lang in enumerate(accept_langs):
        l = lang.split(';', 2)

        # If not supplied, quality defaults to 1...
        quality = 1.0

        if len(l) == 2:
            q = l[1]
            if q.startswith('q='):
                q = q.split('=', 2)[1]
                try:
                    quality = float(q)
                except ValueError:
                    # malformed quality value, skip it.
                    continue

        if quality == 1.0:
            # ... but we use 1.9 - 0.001 * position to
            # keep the ordering between all items with
            # 1.0 quality, which may include items with no quality
            # defined, and items with quality defined as 1.
            quality = 1.9 - (0.001 * index)

        accepts.append((quality, l[0]))

    # Filter langs with q=0, which means
    # unwanted lang according to the spec
    # See: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4
    accepts = [acc for acc in accepts if acc[0]]

    accepts.sort()
    accepts.reverse()

    return [lang for quality, lang in accepts]
    
def normalize_lang(lang):
    lang = lang.strip().lower()
    lang = lang.replace('_', '-')
    lang = lang.replace(' ', '')
    return lang

def normalize_langs(langs):
    # Make a mapping from normalized->original so we keep can match
    # the normalized lang and return the original string.
    n_langs = {}
    for l in langs:
        n_langs[normalize_lang(l)] = l
    return n_langs

def locale_negotiator(request):
    
    settings = get_settings()
    available_languages = settings.get('available_languages', '').split()
    preferred_languages = get_preferred_languages(request)
    
    available_languages = normalize_langs(available_languages)
    for lang in preferred_languages:
        if lang in available_languages:
            return available_languages.get(lang)
        # If the user asked for a specific variation, but we don't
        # have it available we may serve the most generic one,
        # according to the spec (eg: user asks for ('en-us',
        # 'de'), but we don't have 'en-us', then 'en' is preferred
        # to 'de').
        parts = lang.split('-')
        if len(parts) > 1 and parts[0] in available_languages:
            return available_languages.get(parts[0])
            
    return settings.get('default_locale_name', 'en')
