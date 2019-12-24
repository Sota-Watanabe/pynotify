import subprocess


class NotificationError(Exception):
    pass


class BaseNotification:
    # Main
    def notify(self):
        raise NotImplementedError()


class WebhookNotification(BaseNotification):
    '''
    WebhookNotification:
        Webhook による通知
    引数:
        message(str): 本文
        url(str): Webhook の URL
    '''
    def __init__(self, message, url):
        self._message = None
        self._url = None
        self.set_message(message)
        self.set_url(url)

    # message のプロパティ用
    def get_message(self):
        return self._message

    def set_message(self, message):
        if isinstance(message, str):
            self._message = message
        else:
            raise NotificationError(
                f'message can only set str (not \"{type(message)}\")'
            )

    message = property(get_message, set_message)

    # url のプロパティ用
    def get_url(self):
        return self._url

    def set_url(self, url):
        if isinstance(url, str):
            self._url = url
        else:
            raise NotificationError(
                f'url can only set str (not \"{type(url)}\")'
            )

    url = property(get_url, set_url)


class BeepNotification(BaseNotification):
    '''
    BeepNotification:
        (macOS 用)ビープ音による通知
    引数:
        times(int): ビープ音の回数
    '''
    def __init__(self, times):
        self._times = None
        self.set_times(times)

    # times のプロパティ用
    def get_times(self):
        return self._times

    def set_times(self, times):
        if isinstance(times, int):
            self._times = times
        else:
            raise NotificationError(
                f'times can only set int (not \"{type(times)}\")'
            )

    times = property(get_times, set_times)

    # 通知の実行
    def notify(self):
        cmd = ['osascript', '-e', f'beep {self.times}']
        subprocess.run(cmd)


class CenterNotification(BaseNotification):
    '''
    CenterNotification:
        (macOS 用)通知センターによる通知
    引数:
        message(str): 本文
        title(str): タイトル
        subtitle(str): サブタイトル
        sound(bool): 音の有無
    '''
    def __init__(self, message, title=None, subtitle=None, sound=True):
        self._message = None
        self._title = None
        self._subtitle = None
        self._sound = None
        self.set_message(message)
        if title:
            self.set_title(title)
        if subtitle:
            self.set_subtitle(subtitle)
        if sound:
            self.set_sound(sound)

    # message のプロパティ用
    def get_message(self):
        return self._message

    def set_message(self, message):
        if isinstance(message, str):
            self._message = message
        else:
            raise NotificationError(
                f'message can only set str (not \"{type(message)}\")'
            )

    message = property(get_message, set_message)

    # title のプロパティ用
    def get_title(self):
        return self._title

    def set_title(self, title):
        if isinstance(title, str):
            self._title = title
        else:
            raise NotificationError(
                f'title can only set str (not \"{type(title)}\")'
            )
        # タイトルとサブタイトルの両方がないといけないため、片方だけ設定された場合、もう一方を空白にする
        if not self._subtitle:
            self._subtitle = ' '

    title = property(get_title, set_title)

    # subtitle のプロパティ用
    def get_subtitle(self):
        return self._subtitle

    def set_subtitle(self, subtitle):
        if isinstance(subtitle, str):
            self._subtitle = subtitle
        else:
            raise NotificationError(
                f'subtitle can only set str (not \"{type(subtitle)}\")'
            )
        # タイトルとサブタイトルの両方がないといけないため、片方だけ設定された場合、もう一方を空白にする
        if not self._title:
            self._title = ' '

    subtitle = property(get_subtitle, set_subtitle)

    # sound のプロパティ用
    def get_sound(self):
        return self._sound

    def set_sound(self, sound):
        if isinstance(sound, bool):
            self._sound = sound
        else:
            raise NotificationError(
                f'sound can only set bool (not \"{type(sound)}\")'
            )

    sound = property(get_sound, set_sound)

    # 通知の実行
    def notify(self):
        _message = f'display notification \"{self._message}\"'
        _title = \
            f'with title \"{self._title}\" subtitle \"{self._subtitle}\"' \
            if self._title and self._subtitle else ''
        _sound = 'sound name \"\"' if self._sound else ''
        cmd = ['osascript', '-e', f'{_message} {_title} {_sound}']
        subprocess.run(cmd)


class SlackNotification(WebhookNotification):
    '''
    SlackNotification:
        Slack による通知
    引数(WebhookNotification):
        message(str): 本文
        url(str): Incoming Webhook の URL
    '''
    # 通知の実行
    def notify(self):
        import json
        import requests
        data = {'text': self._message}
        requests.post(self._url, data=json.dumps(data))


class DiscordNotification(WebhookNotification):
    '''
    DiscordNotification:
        Discord による通知
    引数(WebhookNotification):
        message(str): 本文
        url(str): Discord の Webhook の URL
    '''
    # 通知の実行
    def notify(self):
        import json
        import requests
        data = {'content': self._message}
        requests.post(
            self._url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )


class LineNotification(BaseNotification):
    '''
    LineNotification:
        Line による通知
    引数:
        message(str): 本文
        token(str): LINE Notify のトークン
    '''
    def __init__(self, message, token):
        self.URL = 'https://notify-api.line.me/api/notify'
        self._message = None
        self._token = None
        self.set_message(message)
        self.set_token(token)

    # message のプロパティ用
    def get_message(self):
        return self._message

    def set_message(self, message):
        if isinstance(message, str):
            self._message = message
        else:
            raise NotificationError(
                f'message can only set str (not \"{type(message)}\")'
            )

    message = property(get_message, set_message)

    # token のプロパティ用
    def get_token(self):
        return self._token

    def set_token(self, token):
        if isinstance(token, str):
            self._token = token
        else:
            raise NotificationError(
                f'token can only set str (not \"{type(token)}\")'
            )

    token = property(get_token, set_token)

    # 通知の実行
    def notify(self):
        import requests
        headers = {'Authorization': f'Bearer {self._token}'}
        params = {'message': self._message}
        requests.post(
            self.URL,
            headers=headers,
            params=params
        )