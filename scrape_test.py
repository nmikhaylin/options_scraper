import tensorflow as tf

import scrape

test  = tf.test
log = tf.logging
FLAGS = tf.flags.FLAGS


class ScraperTest(test.TestCase):
  def testExtractDict(self):
    with self.test_session():
      bracket_string = """
        blah { { } , { asdasda. } , {  { }} } blah
      """
      match = scrape.extract_dict(bracket_string, 7)
      self.assertEquals(match, "{ { } , { asdasda. } , {  { }} }")

  def testExtractDictAtBeg(self):
    with self.test_session():
      bracket_string = "{ { } , { asdasda. } , {  { }} } blah"
      match = scrape.extract_dict(bracket_string, 0)
      self.assertEquals(match, "{ { } , { asdasda. } , {  { }} }")

  def testFindKeySimpleNested(self):
    with self.test_session():
      d = {"a": {"b": {"c": 1}}}
      res = scrape.find_key(d, "c")
      self.assertEqual(res, ["a:b:c"])

  def testFindKeySimpleTopLevel(self):
    with self.test_session():
      d = {"a": {"b": {"c": 1}}}
      res = scrape.find_key(d, "a")
      self.assertEqual(res, ["a"])

  def testFindKeyNestedMultiple(self):
    with self.test_session():
      d = {"a": {"b": {"c": 1}, "d": {"c": 2}}}
      res = scrape.find_key(d, "c")
      self.assertEqual(res, ["a:b:c", "a:d:c"])

if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  test.main()
