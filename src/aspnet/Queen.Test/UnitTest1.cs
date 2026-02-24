namespace Queen.Test;

public class UnitTest1
{
    [Fact]
    public void Test1()
    {
        Assert.True(true);
    }

    [Fact]
    public void Test2()
    {
        Assert.False(false);
    }

    [Fact]
    public void Test3()
    {
        Assert.Equal(1, 1);
    }

    [Fact]
    public void Test4()
    {
        Assert.NotEqual(1, 2);
    }

    [Fact]
    public void Test5()
    {
        Assert.NotNull(null);
    }

    [Fact]
    public void Test6()
    {
        Assert.Null(null);
    }

    [Fact]
    public void Test7()
    {
        Assert.Contains(1, new[] { 1, 2, 3 });
    }

    [Fact]
    public void Test8()
    {
        Assert.DoesNotContain(4, new[] { 1, 2, 3 });
    }

}
