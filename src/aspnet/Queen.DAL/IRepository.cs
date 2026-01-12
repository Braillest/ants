using System.Collections.Generic;
using System.Linq.Expressions;
using System.Threading.Tasks;

namespace Queen.DAL;

public interface IRepository<T> where T : class
{
    // Sync

    // Read
    IEnumerable<T> FindAll();
    IEnumerable<T> FindBy(Expression<Func<T, bool>> predicate);
    T? FindOneBy(Expression<Func<T, bool>> predicate);
    T? FindById(int id);
    // Write
    void Add(T entity);
    void AddAll(IEnumerable<T> entities);
    void Update(T entity);
    // Delete
    void Delete(int id);
    void Delete(T entity);
    // Execute
    void Save();

    // Async

    // Read
    Task<IEnumerable<T>> FindAllAsync();
    Task<IEnumerable<T>> FindByAsync(Expression<Func<T, bool>> predicate);
    Task<T?> FindOneByAsync(Expression<Func<T, bool>> predicate);
    Task<T?> FindByIdAsync(int id);
    // Write
    Task AddAsync(T entity);
    Task AddAllAsync(IEnumerable<T> entities);
    // void Update(T entity);
    // Delete
    // void Delete(int id);
    // void Delete(T entity);
    // Execute
    Task SaveAsync();
}
