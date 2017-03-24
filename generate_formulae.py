import re
import requests
from lxml import html
from hashlib import sha256
from joblib import Parallel, delayed

def versions(tree):
    for link in tree.xpath('//a/@href'):
        match = re.search('https://services.gradle.org/distributions/gradle-(.*)-all.zip', link)
        try:
            yield match.group(1)
        except:
            pass

def gen_file_content(version):
    link = "https://downloads.gradle.org/distributions/gradle-{}-all.zip".format(version)
    print("fetching distribution for {}".format(version))
    f = requests.get(link)
    checksum = sha256(f.content).hexdigest()
    print("sha256sum: {}".format(checksum))
    return '''class GradleAT{} < Formula
  desc "Build system based on the Groovy language"
  homepage "https://www.gradle.org/"
  url "https://downloads.gradle.org/distributions/gradle-{}-all.zip"
  sha256 "{}"

  bottle :unneeded

  option "with-all", "Installs Javadoc, examples, and source in addition to the binaries"

  depends_on :java => "1.7+"

  def install
    libexec.install %w[bin lib]
    libexec.install %w[docs media samples src] if build.with? "all"
    bin.install_symlink libexec/"bin/gradle"
  end

  test do
    ENV.java_cache
    assert_match version.to_s, shell_output("#{{bin}}/gradle --version")
  end
end'''.format(version.replace(".", ""), version, checksum)

def write_formula(version):
    print("Found version {}".format(version))
    formula = gen_file_content(version)
    with open('./Formula/gradle@{}.rb'.format(version), 'w') as f:
        f.write(formula)

if __name__ == '__main__':
    page = requests.get("https://gradle.org/releases")
    tree = html.fromstring(page.content)
    Parallel(n_jobs=4)(delayed(write_formula)(v) for v in versions(tree))
