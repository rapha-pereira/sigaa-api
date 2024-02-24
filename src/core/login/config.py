"""A module to represent the login configuration constants."""

RECAPTCHA_ANCHOR: str = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcbx1MaAAAAAHvwThwws5-sAL-VcBhlenk9L0q1&co=aHR0cHM6Ly9zaWdhYS5pZnNjLmVkdS5icjo0NDM.&hl=pt-BR&v=1kRDYC3bfA-o6-tsWzIBvp7k&size=invisible&sa=LoginUnificado&cb=6an25rsccy1a"
RECAPTCHA_RELOAD: str = "https://www.google.com/recaptcha/api2/reload?k=6Lcbx1MaAAAAAHvwThwws5-sAL-VcBhlenk9L0q1"
RECAPTCHA_PAYLOAD: str = "v=1kRDYC3bfA-o6-tsWzIBvp7k&reason=q&c=<token>&k=6Lcbx1MaAAAAAHvwThwws5-sAL-VcBhlenk9L0q1&co=aHR0cHM6Ly9zaWdhYS5pZnNjLmVkdS5icjo0NDM.&hl=en&size=invisible&chr=&vh=&bg="

SIGAA_BASE_URL: str = "https://sig.ifsc.edu.br/sigaa"
SIGAA_LOGIN_URL: str = "verTelaLogin.do"
SIGAA_LOGIN_FORM_URL: str = "logar.do?dispatch=logOn"

SIGAA_LOGIN_FORM_HEADER: str = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "873",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "sig.ifsc.edu.br",
    "Origin": "https://sig.ifsc.edu.br",
    "Referer": "https://sig.ifsc.edu.br/sigaa/verTelaLogin.do",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
}
