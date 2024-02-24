"""A module to represent the login configuration constants."""

RECAPTCHA_ANCHOR: str = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcbx1MaAAAAAHvwThwws5-sAL-VcBhlenk9L0q1&co=aHR0cHM6Ly9zaWdhYS5pZnNjLmVkdS5icjo0NDM.&hl=pt-BR&v=1kRDYC3bfA-o6-tsWzIBvp7k&size=invisible&sa=LoginUnificado&cb=6an25rsccy1a"
RECAPTCHA_RELOAD: str = "https://www.google.com/recaptcha/api2/reload?k=6Lcbx1MaAAAAAHvwThwws5-sAL-VcBhlenk9L0q1"
RECAPTCHA_PAYLOAD: str = "v=1kRDYC3bfA-o6-tsWzIBvp7k&reason=q&c=<token>&k=6Lcbx1MaAAAAAHvwThwws5-sAL-VcBhlenk9L0q1&co=aHR0cHM6Ly9zaWdhYS5pZnNjLmVkdS5icjo0NDM.&hl=en&size=invisible&chr=&vh=&bg="

SIGAA_BASE_URL: str = "https://sigaa.ifsc.edu.br/sigaa"
SIGAA_LOGIN_URL: str = "verTelaLogin.do"
SIGAA_LOGIN_FORM_URL: str = "logar.do?dispatch=logOn"

SIGAA_LOGIN_FORM_HEADER: str = {
    "Host": "sigaa.ifsc.edu.br",
    "User-Agent": "SIGAA_API/1.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "829",
    "Origin": "https://sigaa.ifsc.edu.br",
    "Connection": "keep-alive",
    "Referer": f"{SIGAA_BASE_URL}/{SIGAA_LOGIN_URL}",
    # "Cookie": request_cookies["JSESSIONID"],
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
}
