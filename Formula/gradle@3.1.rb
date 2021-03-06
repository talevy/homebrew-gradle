class GradleAT31 < Formula
  desc "Build system based on the Groovy language"
  homepage "https://www.gradle.org/"
  url "https://downloads.gradle.org/distributions/gradle-3.1-all.zip"
  sha256 "43be380834a13e28e9504c21f67fe1a8895ab54f314a6596601896dca7213482"

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
    assert_match version.to_s, shell_output("#{bin}/gradle --version")
  end
end